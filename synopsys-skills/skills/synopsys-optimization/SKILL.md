---
name: synopsys-optimization
description: Use when improving Synopsys implementation power, timing, area, congestion, clock quality, buffering, or signal integrity through controlled measured experiments.
---

# Controlled PPA optimization

Read [execution contract](../../references/execution-contract.md), the owning tool
skill and each proposed command/option manual. Preserve RTL, SDC, hard objectives,
required corners and verification coverage. Establish a valid baseline with
metrics, units, input/corner/activity provenance and an immutable checkpoint.
Power estimates from different activity or corner assumptions are not comparable.

Identify the limiting metric and its physical cause. Propose one bounded change
with old/new values, a report-supported hypothesis and a documented supported
parameter. Dependencies matter: density affects congestion/area/wirelength; buffering
affects slew/load/power/area; CTS affects setup and hold; routing/SI choices affect
delay/coupling. Missing licenses/libraries and formal failures need diagnosis,
not parameter search. See [troubleshooting](../synopsys-troubleshooting/SKILL.md).

Examples of allowed experiments, after setting design-specific bounds:

- DC map effort medium/high or documented synthesis effort strategy; recheck formal.
- Core utilization within approved floorplan/die limits; rerun floorplan through signoff.
- Version-checked placement/congestion/clock/routing options; rerun all affected stages.
- Permitted cell/buffer strategy with complete setup/hold/power/SI checks.

Capture option defaults and current values before mutation. Never infer an app
option name, use an obsolete option silently, or combine incompatible switches.
Parameter JSON is passed as SNPS_PARAM_parameter_name environment values; Tcl
adapters use `snps_parameter` to apply exactly the recorded value. A recorded
change that is never applied by the script is not an optimization experiment.

```sh
python3 scripts/optimize.py /absolute/baseline.manifest.json /absolute/optimization-plan.json --out /absolute/runs/design/optimization-001
```

The driver runs the baseline and a bounded candidate list, validates each old/new
value against the accepted configuration, reruns the complete selected verification
chain, compares hard limits and guardrails, and updates the best pointer only for
sufficient improvement. Rejected runs remain intact. Full mode rechecks formal and
all signoff stages. `--partial` limits the evidence to the selected stage experiment.
An infeasible baseline needs diagnosis/repair before this feasible-PPA optimizer;
use stage recovery to resolve negative slack, without promoting failing results.

Set `max_trials`, wall budget, `max_no_improvement`, an objective/direction,
absolute/relative improvement thresholds, every hard metric limit and regression
guardrails. Missing/nonfinite metrics reject the candidate. Area/library units
and estimated/report-limited slack must be labeled accurately. Metrics extraction
from [reports.py](../../scripts/reports.py) produces candidates with provenance;
it does not establish path coverage or signoff closure.

A clock-target change is a requirements revision requiring explicit user permission
and a new baseline/specification, not a hidden change in this optimization loop.
Final acceptance requires functional correctness, required verification and all
hard constraints. Return the best valid run, comparison evidence and rejected
changes, or report that no candidate exceeded the configured threshold.
