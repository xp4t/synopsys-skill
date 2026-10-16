"""Fail-closed promotion and bounded implementation parameter decisions."""
import math
from pathlib import Path

CHECKS = {
 'rtl': ['rtl_elaborated','rtl_checked'],
 'constraints': ['clocks_valid','io_delays_valid','exceptions_reviewed','no_unconstrained_paths'],
 'synthesis': ['mapped','design_checks_clean','constraints_preserved'],
 'formal': ['equivalence','proof_coverage_clean'],
 'floorplan': ['technology_linked','floorplan_legal'],
 'power': ['pg_connectivity','pg_drc_clean'],
 'placement': ['placement_legal','congestion_acceptable'],
 'cts': ['clock_connectivity','skew_acceptable','setup_hold_analyzed'],
 'routing': ['no_unrouted_nets','route_drc_clean'],
 'extraction': ['parasitics_complete','rc_corner_correct'],
 'timing': ['setup_clean','hold_clean','no_unconstrained_paths','corners_complete'],
 'physical': ['drc_clean','lvs_clean','antenna_clean','power_signal_connectivity'],
 'streamout': ['layer_map_valid','cell_views_complete','stream_integrity',
               'final_stream_drc_clean','final_stream_lvs_clean','final_stream_antenna_clean'],
}
FORBIDDEN = {'clock_period_ns','rtl','sdc','top','functionality','false_paths','multicycle_paths',
             'required_checks','voltage','temperature','corners','signoff_required'}
NON_TUNING = {'license','environment','missing_input','library','rtl','constraints','formal','invalid_command','technology','crash','memory','timeout'}


def finite(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value)


def limits_ok(metrics, limits):
    failures=[]
    for key, bound in limits.items():
        value=metrics.get(key)
        if not finite(value):
            failures.append(f'{key}: missing or nonfinite metric')
            continue
        if 'min' in bound and value<bound['min']:
            failures.append(f'{key}: {value} < {bound["min"]}')
        if 'max' in bound and value>bound['max']:
            failures.append(f'{key}: {value} > {bound["max"]}')
    return failures


def local_artifact(directory, relative):
    root=Path(directory).resolve()
    p=(root/relative).resolve()
    if not p.is_relative_to(root):
        raise ValueError('Artifact/report escapes attempt directory')
    if not p.exists() or (p.is_file() and p.stat().st_size==0):
        raise ValueError(f'Missing/empty artifact: {relative}')
    return p


def validate_result(result, directory, stage, required_artifacts, metric_limits, extra_checks=()):
    if result.get('status')!='pass':
        raise ValueError('Stage did not report pass')
    checks=result.get('checks',{})
    for key in CHECKS.get(stage,[])+list(extra_checks):
        if checks.get(key) is not True:
            raise ValueError(f'Required verification failed or absent: {key}')
    reports=result.get('reports',[])
    if not reports:
        raise ValueError('A passing result needs retained report evidence')
    for name in reports+list(required_artifacts):
        local_artifact(directory,name)
    for name in reports:
        p=local_artifact(directory,name)
        if not p.is_file() or p.stat().st_size==0:
            raise ValueError(f'Report evidence must be a nonempty file: {name}')
    for key,value in result.get('metrics',{}).items():
        if not finite(value):
            raise ValueError(f'Nonfinite or nonnumeric metric: {key}')
    problems=limits_ok(result.get('metrics',{}),metric_limits)
    if problems:
        raise ValueError('; '.join(problems))
    return True


def validate_change(change, parameters, allowed, category):
    key=change['parameter']
    if category in NON_TUNING:
        raise ValueError(f'{category} requires diagnosis/input/environment correction, not PPA tuning')
    if key in FORBIDDEN or key not in allowed:
        raise ValueError(f'Parameter is not authorized for tuning: {key}')
    if key not in parameters or parameters[key]!=change['old']:
        raise ValueError('Original parameter does not match current accepted configuration')
    bound=allowed[key]
    if 'choices' in bound:
        if change['new'] not in bound['choices']:
            raise ValueError('Parameter choice is outside allowed set')
    elif not finite(change['new']) or limits_ok({key:change['new']},{key:bound}):
        raise ValueError('Parameter value is outside allowed bounds')
    return True


def compare(baseline, candidate, policy):
    problems=limits_ok(candidate,policy.get('limits',{}))
    objective=policy['objective']
    a,b=baseline.get(objective),candidate.get(objective)
    if not finite(a) or not finite(b):
        problems.append('Objective metric missing/nonfinite')
    for key, bound in policy.get('guardrails',{}).items():
        old,new=baseline.get(key),candidate.get(key)
        if not finite(old) or not finite(new):
            problems.append(f'{key}: missing guardrail metric')
            continue
        direction=bound.get('direction')
        if direction not in {'min','max'}:
            problems.append(f'{key}: guardrail direction must explicitly be min or max')
            continue
        regression=old-new if direction=='max' else new-old
        if regression>bound.get('max_regression',0):
            problems.append(f'{key}: regression {regression}')
    if problems:
        return {'decision':'revert','reasons':problems}
    improvement=(a-b) if policy.get('direction','min')=='min' else (b-a)
    threshold=max(policy.get('min_absolute_improvement',0),abs(a)*policy.get('min_relative_improvement',0.01))
    return {'decision':'keep' if improvement>0 and improvement>=threshold else 'revert',
            'improvement':improvement,'threshold':threshold,
            'reasons':[] if improvement>=threshold and improvement>0 else ['insufficient improvement']}
