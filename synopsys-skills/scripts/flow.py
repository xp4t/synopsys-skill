#!/usr/bin/env python3
"""Run reviewed stage scripts with retained evidence and fail-closed promotion."""
import argparse
import copy
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import time
import string
import sys

from execution import ROOT, checkpoint, execute, fingerprint, gds_integrity, verify_checkpoint, write_json
from policy import CHECKS, compare, finite, local_artifact, validate_change, validate_result

ORDER=list(CHECKS)
TECH_KEYS=['tech_file','ndm_libraries','rc_models','layer_map','cell_gds','pg_recipe',
           'extraction_recipe','drc_deck','lvs_deck','antenna_deck']


def paths(value):
    return value if isinstance(value,list) else [value]


def preflight(manifest, partial=False):
    errors=[]
    for key in ['design','top','rtl','sdc','requirements','stages']:
        if not manifest.get(key):
            errors.append(f'Missing {key}')
    if not re.fullmatch(r'[A-Za-z0-9_.-]+',manifest.get('design','')):
        errors.append('design must be a simple path-safe identifier')
    for p in paths(manifest.get('rtl',[]))+paths(manifest.get('sdc',[])):
        if not Path(p).is_file():
            errors.append(f'Input file missing: {p}')
    stages=manifest.get('stages',[])
    ids=[s.get('id') for s in stages]
    if len(set(ids))!=len(ids) or any(x not in ORDER for x in ids):
        errors.append('Unknown or duplicate stage id')
    if not partial and ids!=ORDER:
        errors.append('Full flow requires ordered stages: '+', '.join(ORDER))
    for stage in stages:
        if not Path(stage.get('script','')).is_file():
            errors.append(f'{stage.get("id")}: missing reviewed stage script')
        tool=manifest.get('tools',{}).get(stage.get('tool'),{})
        if not tool.get('executable') or not Path(tool['executable']).is_absolute() or not os.access(tool['executable'],os.X_OK):
            errors.append(f'{stage.get("id")}: absolute executable unavailable')
        if stage.get('timeout_s',600)<=0:
            errors.append('Timeout must be positive')
    if not 1<=manifest.get('max_attempts',3)<=20:
        errors.append('max_attempts must be between 1 and 20')
    if not partial:
        technology=manifest.get('technology',{})
        if technology.get('qualified') is not True or not technology.get('qualification_reference'):
            errors.append('technology requires qualification and its provenance reference')
        for key in TECH_KEYS:
            if not technology.get(key):
                errors.append(f'technology missing {key}')
            else:
                for p in paths(technology[key]):
                    if not Path(p).exists():
                        errors.append(f'technology {key} unavailable: {p}')
        for key in ['clock_period_ns','functional_reference','corners','hard_limits']:
            if key not in manifest.get('requirements',{}):
                errors.append(f'requirements missing {key}')
        requirements=manifest.get('requirements',{})
        if not finite(requirements.get('clock_period_ns')) or requirements['clock_period_ns']<=0:
            errors.append('requirements.clock_period_ns must be finite and positive')
        if not requirements.get('corners'):
            errors.append('requirements.corners must explicitly list required signoff corners/modes')
        for key in ['wns_ns','hold_wns_ns']:
            threshold=requirements.get('hard_limits',{}).get(key,{}).get('min')
            if not finite(threshold) or threshold<0:
                errors.append(f'requirements.hard_limits must enforce {key} min >= 0')
        for key in ['ir_em_required']:
            if type(manifest.get('requirements',{}).get(key)) is not bool:
                errors.append('requirements must explicitly specify ir_em_required')
        stream=next((s for s in stages if s['id']=='streamout'),{})
        if not stream.get('gds'):
            errors.append('streamout must name its GDS artifact')
    return errors


def protected_paths(manifest):
    files=paths(manifest.get('rtl',[]))+paths(manifest.get('sdc',[]))
    files+=manifest.get('inputs',[])
    if manifest.get('config_tcl'):
        files.append(manifest['config_tcl'])
    for key,value in manifest.get('technology',{}).items():
        if key in TECH_KEYS:
            files+=paths(value)
    for stage in manifest.get('stages',[]):
        files.append(stage['script'])
        files += [candidate['script'] for candidate in stage.get('recovery_candidates',[])]
    # These helpers are sourced by shipped templates, even in stage copies.
    files.append(str(ROOT/'templates/common.tcl'))
    return list(dict.fromkeys(files))


def run_flow(manifest, directory, partial=False):
    problems=preflight(manifest,partial)
    if problems:
        raise ValueError('\n'.join(problems))
    directory=Path(directory).resolve()
    directory.mkdir(parents=True,exist_ok=False)
    manifest=copy.deepcopy(manifest)
    write_json(directory/'manifest.json',manifest)
    # Preserve declared paths. Hashing only a resolved target misses ordinary
    # source/library symlink retargeting during a run.
    hashes={str(Path(p).absolute()):fingerprint(p) for p in protected_paths(manifest)}
    identities={p:str(Path(p).resolve()) for p in hashes}
    write_json(directory/'input-hashes.json',hashes)
    write_json(directory/'input-identities.json',identities)
    def inputs_unchanged():
        try:
            return all(str(Path(p).resolve())==identities[p] and fingerprint(p)==digest for p,digest in hashes.items())
        except (OSError,ValueError):
            return False
    summary={'status':'running','partial':partial,'attempts':[],'accepted':{},'blockers':[],
             'started_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    parameters=copy.deepcopy(manifest.get('parameters',{}))
    sources=directory/'sources';sources.mkdir()
    start=time.monotonic()
    deadline=start+manifest.get('wall_budget_s',14400)
    incoming=None
    for stage in manifest['stages']:
        sid=stage['id']; previous_categories=[]; variants=iter(stage.get('recovery_candidates',[]))
        license_retries=0; selected=None; accepted=False
        for attempt in range(1,manifest.get('max_attempts',3)+1):
            if time.monotonic()>=deadline:
                summary['blockers'].append('Run wall-clock budget exhausted');break
            if not inputs_unchanged():
                summary['blockers'].append('Protected input changed; invalidate downstream results');break
            if incoming and not verify_checkpoint(incoming):
                summary['blockers'].append('Incoming checkpoint failed integrity verification');break
            changes=[]
            script=stage['script']
            if selected:
                if not selected.get('reason') or not selected.get('documentation'):
                    summary['blockers'].append('Correction needs reason and authoritative documentation');break
                if selected.get('category') not in previous_categories:
                    summary['blockers'].append('Correction category does not match observed diagnosis');break
                changes=selected.get('changes',[])
                try:
                    for change in changes:
                        validate_change(change,parameters,manifest.get('allowed_parameters',{}),selected['category'])
                except ValueError as e:
                    summary['blockers'].append(str(e));break
                script=selected['script']
            candidate_parameters=copy.deepcopy(parameters)
            candidate_parameters.update({x['parameter']:x['new'] for x in changes})
            copied=sources/f'{sid}-{attempt:03d}{Path(script).suffix}'
            shutil.copy2(script,copied)
            tool=manifest['tools'][stage['tool']]
            args=list(tool.get('startup_args',[]))
            if tool.get('script_option'):
                args += [tool['script_option'],str(copied)]
            else:
                args += [str(copied)]
            dest=directory/sid/f'attempt-{attempt:03d}'
            param_file=sources/f'{sid}-{attempt:03d}-parameters.json'
            write_json(param_file,candidate_parameters)
            env={'SNPS_ATTEMPT':str(attempt),'SNPS_STAGE':sid,'SNPS_TOP':manifest['top'],
                 'SNPS_FRAMEWORK_ROOT':str(ROOT),'SNPS_MANIFEST':str(directory/'manifest.json'),
                 'SNPS_PARAMETERS_JSON':str(param_file),'SNPS_INPUT_HASHES':str(directory/'input-hashes.json')}
            for key,value in candidate_parameters.items():
                if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*',key):
                    raise ValueError('Parameter names must be environment-safe identifiers')
                env['SNPS_PARAM_'+key]=str(value)
            if manifest.get('config_tcl'):
                env['SNPS_CONFIG_TCL']=str(Path(manifest['config_tcl']).resolve())
            if incoming:
                incoming_file=sources/f'{sid}-{attempt:03d}-incoming.json'
                write_json(incoming_file,incoming)
                env['SNPS_CHECKPOINT_MANIFEST']=str(incoming_file)
                # Restore into a writable copy. Never modify the accepted checkpoint.
                restore=directory/'restores'/f'{sid}-{attempt:03d}'
                restored=checkpoint([x['path'] for x in incoming['artifacts']],restore)
                env['SNPS_RESTORE_DIR']=str(restore)
            remaining=deadline-time.monotonic()
            if remaining<=0:
                summary['blockers'].append('Run wall-clock budget exhausted before launch');break
            env=dict(tool.get('environment',{}),**env)
            execution=execute(tool['executable'],args,dest,min(stage.get('timeout_s',600),remaining),env)
            record={'stage':sid,'attempt':attempt,'directory':str(dest),'script_sha256':fingerprint(copied),
                    'parameters':candidate_parameters,'changes':changes,'execution':execution,
                    'correction':selected,'decision':'reject'}
            failure=None; normalized=None
            try:
                if not execution['process_ok']:
                    raise ValueError('Tool exit/timeout/error-marker failure')
                if time.monotonic()>deadline:
                    raise ValueError('Run wall-clock budget exhausted')
                if not inputs_unchanged():
                    raise ValueError('Protected inputs changed during stage')
                normalized=json.loads((dest/'result.json').read_text())
                extra=list(stage.get('required_checks',[]))
                if not partial and sid in {'placement','cts','routing'}:
                    extra+=['functional_equivalence']
                if sid=='physical' and manifest.get('requirements',{}).get('ir_em_required'):
                    extra+=['ir_clean','em_clean']
                validate_result(normalized,dest,sid,stage.get('artifacts',[]),stage.get('metric_limits',{}),extra)
                if sid=='streamout':
                    gds=gds_integrity(local_artifact(dest,stage['gds']))
                    if not gds['bgnlib_present']:
                        raise ValueError('GDS BGNLIB missing')
                    record['gds_integrity']=gds
                if stage.get('baseline_metrics'):
                    comparison=compare(stage['baseline_metrics'],normalized.get('metrics',{}),stage['optimization_policy'])
                    record['comparison']=comparison
                    if comparison['decision']!='keep':
                        raise ValueError('PPA regression or insufficient improvement; revert candidate')
                accepted_paths=[local_artifact(dest,p) for p in stage.get('checkpoint_artifacts',[])]
                saved=checkpoint(accepted_paths,directory/'checkpoints'/sid) if accepted_paths else incoming
                record['decision']='accept';record['result']=normalized
                record['evidence_hashes']={p:fingerprint(local_artifact(dest,p)) for p in normalized['reports']+stage.get('artifacts',[])}
                summary['accepted'][sid]={'attempt':attempt,'directory':str(dest),'checkpoint':saved,'result':normalized}
                incoming=saved;parameters=candidate_parameters;accepted=True
            except (ValueError,OSError,KeyError) as e:
                failure=str(e)
                record['failure']=failure
            summary['attempts'].append(record)
            write_json(dest/'decision.json',record)
            if accepted:
                break
            previous_categories=list(execution['failure_categories'])
            if sid=='formal':
                previous_categories.append('formal')
            if not previous_categories:
                previous_categories=['verification']
            if 'license' in previous_categories and license_retries<manifest.get('license_retries',1):
                license_retries+=1
                delay=min(30,max(0,manifest.get('license_backoff_s',0)))
                time.sleep(min(delay,max(0,deadline-time.monotonic())))
                # Exact same script/config, no speculative tuning for licensing.
                continue
            selected=next(variants,None)
            if selected is None:
                summary['blockers'].append(f'{sid}: {failure}; no justified recovery candidate remains')
                break
        if not accepted:
            summary['status']='blocked'
            if not summary['blockers']:
                summary['blockers'].append(f'{sid}: retry budget exhausted')
            break
    else:
        if partial:
            summary['status']='partial-stage-validated'
        else:
            # Final hard limits must be populated by the signoff timing/PPA stage.
            from policy import limits_ok
            metrics=summary['accepted']['timing']['result'].get('metrics',{})
            failures=limits_ok(metrics,manifest['requirements']['hard_limits'])
            if failures:
                summary['status']='blocked';summary['blockers']+=failures
            else:
                summary['status']='end-to-end-validated'
    summary['elapsed_s']=round(time.monotonic()-start,3)
    summary['effective_parameters']=parameters
    effective=copy.deepcopy(manifest)
    effective['parameters']=parameters
    for sid,record in summary['accepted'].items():
        winning=next(x for x in summary['attempts'] if x['stage']==sid and x['attempt']==record['attempt'])
        if winning['correction']:
            for stage in effective['stages']:
                if stage['id']==sid:
                    stage['script']=winning['correction']['script']
                    stage['recovery_candidates']=[]
    write_json(directory/'effective-manifest.json',effective)
    summary['effective_manifest']=str(directory/'effective-manifest.json')
    write_json(directory/'summary.json',summary)
    return summary


def load_manifest(path):
    path=Path(path).absolute()
    variables=dict(os.environ,BUNDLE_ROOT=str(ROOT),MANIFEST_DIR=str(path.parent),PYTHON=sys.executable)
    def expand(value):
        if isinstance(value,str):
            try:return string.Template(value).substitute(variables)
            except (KeyError,ValueError) as e:raise ValueError(f'Unconfigured manifest variable: {e}') from e
        if isinstance(value,list):return [expand(v) for v in value]
        if isinstance(value,dict):return {k:expand(v) for k,v in value.items()}
        return value
    manifest=expand(json.loads(path.read_text()))
    def absolute(value):
        if isinstance(value,list):return [absolute(v) for v in value]
        p=Path(value).expanduser()
        return str(p.absolute() if p.is_absolute() else (path.parent/p).absolute())
    for key in ['rtl','sdc','config_tcl','inputs']:
        if key in manifest:manifest[key]=absolute(manifest[key])
    for key in TECH_KEYS:
        if key in manifest.get('technology',{}):manifest['technology'][key]=absolute(manifest['technology'][key])
    for stage in manifest.get('stages',[]):
        stage['script']=absolute(stage['script'])
        for candidate in stage.get('recovery_candidates',[]):candidate['script']=absolute(candidate['script'])
    for tool in manifest.get('tools',{}).values():
        executable=tool.get('executable','')
        if '/' in executable and not Path(executable).is_absolute():executable=absolute(executable)
        found=shutil.which(executable)
        # Leave an unresolved basename for preflight to report as unavailable.
        tool['executable']=str(Path(found).absolute()) if found else executable
    return manifest


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    sub=ap.add_subparsers(dest='command',required=True)
    p=sub.add_parser('preflight');p.add_argument('manifest',type=Path);p.add_argument('--partial',action='store_true')
    p=sub.add_parser('run');p.add_argument('manifest',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--partial',action='store_true')
    p=sub.add_parser('diagnose');p.add_argument('log',type=Path)
    p=sub.add_parser('compare');p.add_argument('baseline',type=Path);p.add_argument('candidate',type=Path);p.add_argument('policy',type=Path)
    args=ap.parse_args()
    if args.command=='diagnose':
        from execution import classify
        print(json.dumps({'categories':classify(args.log.read_text(errors='replace')),'triage_only':True},indent=2));return
    if args.command=='compare':
        print(json.dumps(compare(*[json.loads(p.read_text()) for p in (args.baseline,args.candidate,args.policy)]),indent=2));return
    manifest=load_manifest(args.manifest)
    if args.command=='preflight':
        errors=preflight(manifest,args.partial)
        print(json.dumps({'ready':not errors,'blockers':errors},indent=2))
        raise SystemExit(2 if errors else 0)
    result=run_flow(manifest,args.out,args.partial)
    print(json.dumps({'status':result['status'],'blockers':result['blockers'],'summary':str(args.out/'summary.json')},indent=2))
    raise SystemExit(2 if result['status']=='blocked' else 0)


if __name__=='__main__':
    main()
