#!/usr/bin/env python3
"""Read-only installation discovery; never executes discovered binaries."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = {
    'dc_shell': ('design-compiler', 'tcl', '-f'),
    'design_vision': ('design-vision', 'tcl-gui', '-f'),
    'icc_shell': ('ic-compiler', 'tcl', '-f'),
    'icc2_shell': ('ic-compiler-ii', 'tcl', '-file'),
    'fc_shell': ('fusion-compiler', 'tcl', '-file'),
    'pt_shell': ('primetime', 'tcl', '-file'),
    'fm_shell': ('formality', 'tcl', '-file'),
    'vcs': ('vcs', 'compiler', None),
    'verdi': ('verdi', 'tcl-gui', None),
    'StarXtract': ('starrc', 'command-file', None),
    'icv': ('ic-validator', 'runset', None),
    'hspice': ('hspice', 'spice', None),
    'custom_compiler': ('custom-compiler', 'tcl-gui', None),
    'vc_static_shell': ('vc-static', 'tcl', None),
    'spyglass': ('spyglass', 'unknown', None),
    'lc_shell': ('library-compiler', 'tcl', None),
    'icc2_lm_shell': ('ndm-library-manager', 'tcl', '-file'),
    'vcps': ('vc-portable-stimulus', 'compiler', None),
    'starrc_shell': ('starrc-shell', 'tcl', '-file'),
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def discover(root):
    root = Path(root).resolve()
    # All file names are examined, including embedded products. No symlink traversal.
    executables, libraries, documents, setups, manifests = [], [], [], [], []
    errors = []
    def error(e):
        errors.append(str(e))
    for directory, dirs, files in os.walk(root, onerror=error):
        for name in files:
            p = Path(directory) / name
            parts = p.relative_to(root).parts
            if 'bin' in parts and os.access(p, os.X_OK):
                executables.append(str(p))
            if p.suffix.lower() in {'.db', '.lib', '.ndm', '.tf', '.tluplus', '.nxtgrd', '.itf', '.lef', '.gds', '.gdsii'}:
                libraries.append({'path': str(p), 'kind': p.suffix.lower(),
                                  'qualification': 'unqualified; sample/internal files are not a foundry PDK'})
            if name.endswith(('.pdf', '.info')) and 'doc' in parts:
                documents.append(str(p))
            if (name.endswith(('.csh', '.sh')) and re.search('setup|environ|start', name, re.I)) or name == 'synopsys_start':
                setups.append(str(p))
            if '.installer' in parts and len(parts) < 7:
                manifests.append(str(p))
    installations = []
    for product in sorted(root.iterdir()):
        if not product.is_dir() or product.name in {'doc', 'install_bin'} or product.name.startswith('snps_installer_temp_'):
            continue
        for directory, dirs, files in os.walk(product):
            p = Path(directory)
            if re.match(r'^[A-Z]-\d{4}\.\d{2}|^\d+\.\d+$', p.name):
                installations.append({'directory': str(p), 'product_directory': product.name,
                                      'directory_version': p.name,
                                      'version_evidence': 'directory label, not executed build',
                                      'documentation': sorted(x for x in documents if x.startswith(str(p) + '/'))})
                dirs[:] = []
            elif len(p.relative_to(product).parts) >= 2:
                dirs[:] = []
    tools = []
    for pstr in sorted(executables):
        p = Path(pstr)
        if p.name not in PRIMARY:
            continue
        # Keep canonical wrappers plus embedded products, but exclude architecture replicas.
        if p.parent.name != 'bin' or any(x in p.parts for x in ('linux64', 'linux', 'linuxaarch64', 'aarch64', 'linux64_starrc', 'linuxppc64_starrc', 'platform')):
            continue
        skill, mode, batch = PRIMARY[p.name]
        install = next((x for x in installations if pstr.startswith(x['directory'] + '/')), None)
        version_root = install['directory'] if install else str(p.parent.parent)
        docs = str(Path(version_root) / 'doc')
        tools.append({'id': skill, 'executable': pstr, 'realpath': str(p.resolve()),
                      'executable_sha256': sha(p), 'directory_version': Path(version_root).name,
                      'installation': version_root, 'shell_mode': mode,
                      'batch_script_option': batch, 'batch_option_evidence': 'must verify against indexed invocation manual',
                      'environment': {'license_variable': 'SNPSLMD_LICENSE_FILE',
                                      'setup_policy': 'inherit user-configured environment; no prescribed shell'},
                      'documentation_root': docs if Path(docs).exists() else None,
                      'execution_status': 'not-probed'})
    return {'schema_version': 1, 'discovered_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'root': str(root), 'installations': installations, 'tools': tools,
            'all_bin_executables': executables, 'technology_candidates': libraries,
            'documents': documents, 'setup_candidates': setups, 'installer_records': manifests,
            'scan_errors': errors,
            'absent_primary_executables': sorted(set(PRIMARY) - {Path(x['executable']).name for x in tools}),
            'license': {'availability': 'not established by filesystem discovery; use user-provided configuration'}}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', required=True,help='Local installation root, supplied by the user')
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    data = discover(args.root)
    # Refuse to replace earlier discovery results.
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as f:
        json.dump(data, f, indent=2)
        f.write('\n')
    print(json.dumps({k: len(data[k]) for k in ('installations', 'tools', 'all_bin_executables', 'technology_candidates', 'documents')}))


if __name__ == '__main__':
    main()
