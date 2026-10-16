#!/usr/bin/env python3
"""Bounded PPA experiments; rerun verification after every implementation change."""
import argparse
import copy
import json
from pathlib import Path
import time

from execution import fingerprint, write_json
from flow import load_manifest, protected_paths, run_flow
from policy import compare, validate_change


def metrics_for(summary, stage):
    if stage not in summary['accepted']:
        raise ValueError('Optimization metrics stage did not pass its verification gates')
    return summary['accepted'][stage]['result']['metrics']


def optimize(manifest, plan, directory, partial=False):
    directory=Path(directory).resolve();directory.mkdir(parents=True,exist_ok=False)
    write_json(directory/'optimization-plan.json',plan)
    start=time.monotonic();deadline=start+plan.get('wall_budget_s',3600)
    pinned={p:fingerprint(p) for p in protected_paths(manifest)}
    def bounded_flow(config, destination):
        remaining=deadline-time.monotonic()
        if remaining<=0:
            raise ValueError('Optimization wall-clock budget exhausted')
        config=copy.deepcopy(config)
        config['wall_budget_s']=min(config.get('wall_budget_s',14400),remaining)
        return run_flow(config,destination,partial)
    baseline=bounded_flow(manifest,directory/'baseline')
    if baseline['status']=='blocked':
        result={'status':'blocked','reason':'Baseline needs diagnosis before feasible PPA optimization',
                'baseline':str(directory/'baseline/summary.json')}
        write_json(directory/'optimization-summary.json',result);return result
    metric_stage=plan.get('metric_stage','timing')
    best_metrics=metrics_for(baseline,metric_stage)
    best_manifest=load_manifest(baseline['effective_manifest']);best_run='baseline'
    history=[];stagnation=0
    max_trials=min(20,max(0,int(plan.get('max_trials',4))))
    for index,candidate in enumerate(plan.get('candidates',[])[:max_trials],1):
        if time.monotonic()>=deadline or stagnation>=plan.get('max_no_improvement',2):
            break
        if any(fingerprint(p)!=h for p,h in pinned.items()):
            raise ValueError('Protected inputs changed during optimization')
        if not candidate.get('reason') or not candidate.get('documentation') or not candidate.get('changes'):
            raise ValueError('Each experiment needs changes, reason and documentation')
        trial=copy.deepcopy(best_manifest)
        for change in candidate['changes']:
            validate_change(change,trial.get('parameters',{}),trial.get('allowed_parameters',{}),candidate['category'])
            trial['parameters'][change['parameter']]=change['new']
        # Scripts, requirements, RTL, SDC, corners and technology stay pinned.
        # Re-running the complete selected stage list invalidates stale downstream
        # results, including Formality when synthesis or an ECO changes a netlist.
        label=f'trial-{index:03d}'
        summary=bounded_flow(trial,directory/label)
        decision={'decision':'revert','reasons':['verification gate failed']}
        if summary['status']!='blocked':
            current=metrics_for(summary,metric_stage)
            decision=compare(best_metrics,current,plan['policy'])
            if decision['decision']=='keep':
                best_manifest=load_manifest(summary['effective_manifest']);best_metrics=current;best_run=label;stagnation=0
            else:
                stagnation+=1
        else:
            stagnation+=1
        history.append({'run':label,'candidate':candidate,'decision':decision,'status':summary['status']})
    result={'status':'optimization-finished','best_run':best_run,'metrics':best_metrics,
            'parameters':best_manifest.get('parameters',{}),'trials':history,
            'evidence_scope':'partial stages' if partial else 'full verification chain'}
    write_json(directory/'optimization-summary.json',result)
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('manifest',type=Path);ap.add_argument('plan',type=Path)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--partial',action='store_true')
    args=ap.parse_args()
    result=optimize(load_manifest(args.manifest),json.loads(args.plan.read_text()),args.out,args.partial)
    print(json.dumps(result,indent=2))
    raise SystemExit(2 if result['status']=='blocked' else 0)


if __name__=='__main__':
    main()
