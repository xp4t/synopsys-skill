"""Process isolation, evidence, checkpoints and diagnostic triage."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    'license': r'(?:license.*(?:fail|not available|denied|checkout|check.out)|unable to.*license|FLEXnet Licensing error)',
    'environment': r'(?:error while loading shared libraries|version [`\w.]+.*not found|required by|VC_STATIC_HOME not set)',
    'invalid_command': r'(?:unknown command|invalid command name|unknown option|CMD-005|CMD-010)',
    'missing_input': r'(?:cannot open|could not open|no such file|file.*not found)',
    'library': r'(?:PT-063|library.*(?:not found|not set|missing)|unresolved reference|unresolved cell)',
    'rtl': r'(?:elaboration.*fail|syntax error|multiple driver|inferred latch)',
    'constraints': r'(?:unconstrained|no clock|invalid.*constraint)',
    'formal': r'(?:verification.*fail|equivalence.*fail|failing compare point)',
    'memory': r'(?:out of memory|cannot allocate memory|bad_alloc|oom.kill)',
    'crash': r'(?:segmentation fault|core dumped|internal error|fatal signal)',
    'timing': r'(?:negative slack|timing.*violat|slack.*VIOLATED)',
    'congestion': r'(?:congestion|overflow.*routing)',
    'cts': r'(?:clock.tree.*fail|clock.*disconnected)',
    'routing': r'(?:route.*fail|unrouted net)',
    'drc': r'(?:DRC.*violat|design.rule.*violat)',
    'lvs': r'(?:LVS.*(?:fail|mismatch)|netlist.*mismatch)',
    'technology': r'(?:unsupported.*(?:technology|layer)|missing.*(?:technology|layer.map))',
}
# Anchored severity checks avoid treating prose in the copyright/license banner as failure.
ERROR_RE = re.compile(r'^\s*(?:Error:|Error-\[[^]]+\]|Fatal(?: error)?:|\*\*Error|\*ERROR\*|SNPS_STAGE_ERROR\b)|error while loading shared libraries|: version .*not found', re.I | re.M)


def write_json(path, value):
    with Path(path).open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True, allow_nan=False)
        f.write('\n')


def fingerprint(path):
    p = Path(path).resolve()
    if p.is_symlink():
        raise ValueError('Unexpected symlink')
    if p.is_file():
        h = hashlib.sha256()
        with p.open('rb') as f:
            for block in iter(lambda: f.read(1024*1024), b''):
                h.update(block)
        return h.hexdigest()
    if p.is_dir():
        h = hashlib.sha256()
        for f in sorted(p.rglob('*')):
            if f.is_symlink():
                raise ValueError('Checkpoint trees must not contain symbolic links')
            h.update(str(f.relative_to(p)).encode())
            h.update(b'\0')
            if f.is_file():
                h.update(fingerprint(f).encode())
        return h.hexdigest()
    raise FileNotFoundError(p)


def classify(text):
    return [name for name, pattern in PATTERNS.items() if re.search(pattern, text, re.I)]


def execute(executable, args, directory, timeout_s=600, extra_env=None):
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=False)
    # Synopsys dispatchers select the product from argv[0]. Dereferencing
    # dc_shell -> snps_shell changes the invocation and breaks dispatch.
    resolved=shutil.which(str(executable))
    if not resolved:
        raise ValueError(f'Executable unavailable in configured environment: {executable}')
    executable = str(Path(resolved).absolute())
    if not os.access(executable, os.X_OK):
        raise ValueError(f'Not executable: {executable}')
    argv = [executable] + [str(x) for x in args]
    env = dict(os.environ)
    env.update({str(k): str(v) for k,v in (extra_env or {}).items()})
    start = time.monotonic()
    timed_out = False
    write_json(directory/'invocation.json', {'argv': argv, 'executable_sha256': fingerprint(executable),
               'cwd': str(directory), 'timeout_s': timeout_s, 'environment': {
                   k: ('<configured>' if 'LICENSE' in k or any(x in k for x in ('TOKEN','SECRET','PASSWORD','KEY')) else env[k])
                   for k in sorted(env) if k.startswith(('SNPS_', 'VCS_', 'VERDI_', 'VC_STATIC_')) or k in {'SNPSLMD_LICENSE_FILE','LM_LICENSE_FILE','LD_LIBRARY_PATH','LANG'}},
               'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat()})
    with (directory/'console.log').open('xb') as output:
        proc = subprocess.Popen(argv, cwd=directory, env=env, stdout=output, stderr=subprocess.STDOUT,
                                stdin=subprocess.DEVNULL, start_new_session=True)
        try:
            code = proc.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                code = proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                code = None
            finally:
                # The dispatcher can exit while helpers survive SIGTERM. Kill
                # the owned process group regardless of the parent's state.
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                code = proc.wait()
    log = (directory/'console.log').read_text(errors='replace')
    errors = [m.group(0) for m in ERROR_RE.finditer(log)]
    categories = classify(log)
    if timed_out:
        categories.append('timeout')
    result = {'returncode': code, 'timed_out': timed_out, 'elapsed_s': round(time.monotonic()-start, 3),
              'process_ok': code == 0 and not timed_out and not errors,
              'error_markers': errors, 'failure_categories': categories,
              'log': str(directory/'console.log'), 'log_sha256': fingerprint(directory/'console.log')}
    write_json(directory/'execution.json', result)
    return result


def checkpoint(paths, destination):
    dest = Path(destination).resolve()
    dest.mkdir(parents=True, exist_ok=False)
    records = []
    names = set()
    for source in map(Path, paths):
        if source.name in names:
            raise ValueError('Checkpoint basenames collide')
        names.add(source.name)
        before = fingerprint(source)
        target = dest/source.name
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
        if fingerprint(target) != before or fingerprint(source) != before:
            raise ValueError('Checkpoint changed during copy')
        records.append({'source':str(source.resolve()),'path':str(target),'sha256':before})
    result={'artifacts':records,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    write_json(dest/'checkpoint.json',result)
    return result


def verify_checkpoint(record):
    try:
        return bool(record['artifacts']) and all(fingerprint(x['path']) == x['sha256'] for x in record['artifacts'])
    except (OSError, ValueError):
        return False


def gds_integrity(path):
    """Validate record boundaries, HEADER/BGNLIB/ENDLIB. Not geometry or signoff."""
    p=Path(path)
    count=0; first=None; last=None; bgn=False
    with p.open('rb') as f:
        while True:
            header=f.read(4)
            if not header:
                break
            if len(header)!=4:
                raise ValueError('Truncated GDS header')
            length=int.from_bytes(header[:2],'big')
            if length<4 or length%2 or len(f.read(length-4))!=length-4:
                raise ValueError('Invalid/truncated GDS record')
            record=header[2:]
            if first is None:
                first=record
            if record==b'\x01\x02':
                bgn=True
            if last==b'\x04\x00':
                raise ValueError('Data follows GDS ENDLIB')
            last=record;count+=1
    if first!=b'\x00\x02' or last!=b'\x04\x00':
        raise ValueError('GDS HEADER or ENDLIB missing')
    # A minimal record fixture can test framing, but real stream-out also needs BGNLIB.
    return {'structural_records_only':True,'bgnlib_present':bgn,'records':count,'bytes':p.stat().st_size,'sha256':fingerprint(p)}
