---
name: synopsys-rtl2gds
description: Use when asked to generate GDSII from RTL, run a complete Synopsys ASIC implementation, recover failing stages, or optimize an RTL-to-GDSII flow.
---

# Autonomous RTL-to-GDSII engineering

Operate as the implementation engineer: inspect evidence, choose documented
commands, run controlled experiments and verify results. Read
[execution contract](../../references/execution-contract.md) and
[technology intake](../../references/technology-intake.md) before planning a run.
Use [environment](../synopsys-environment/SKILL.md) and load the next relevant tool
skill. This orchestration supports reasoning and execution; it does not supply a
foundry-qualified technology methodology where none exists.

## Intake and plan

Inventory the user's design without changing it. Enumerate ordered RTL files,
languages, includes/defines, parameters, hierarchy, candidate tops, clocks/resets,
testbenches and existing constraints. Confirm intended top/reset/functionality
where ambiguous. Hash the original RTL and SDC. Record what establishes functional
intent: tests/assertions/specification; equivalence alone preserves only the
reference behavior under its setup assumptions.

Establish explicit clock periods/relationships, IO delay and load assumptions,
operating conditions, exceptions, power/area targets, hard versus soft objectives,
required modes/corners and signoff scope. Missing specifications remain questions
or blockers. Continue independent source/environment checks while awaiting answers.
The counter's 10 ns example is a teaching specification, never a default for a
user design. Do not invent exceptions, frequencies, supply names or foundry rules.

Preflight the technology contract and license/environment evidence. Select
DC+ICC2 or Fusion based on available qualified libraries and user methodology.
Produce a stage/checkpoint plan and manifest with exact tool versions, scripts,
reports, required checks, tunable bounds, retry/time budgets and dependencies.
Read each new command's installed manual and stage prerequisites before scripting.

## Stage gates and handoffs

| Work | Tool and essential actions | Gate and retained handoff |
| --- | --- | --- |
| RTL preparation | VCS regression, DC analyze/elaborate/link/check_design or justified equivalent | Intended top/parameters; no missing hierarchy, unexplained latches/multiple drivers or baseline test failures; source/spec hashes |
| Constraints | DC/implementation/PT clock, IO, exception and unconstrained-path checks | Approved SDC, all required path coverage, no invented false/multicycle paths |
| Synthesis | DC compile or qualified Fusion compile_fusion | Mapped netlist, .ddc/NDM, SDC, SVF, design/timing/area/power reports |
| Equivalence | Formality reference RTL versus exact implementation | Successful complete proof with reviewed setup/constants/abstractions; failures and inconclusive proofs block promotion |
| Floorplan | ICC2/Fusion technology+NDM link, initialize_floorplan, macros/IO/rows/blockages | Legal core/die/sites, consistent libraries/corners, saved library/block |
| Power | Qualified PG patterns/strategy/compile/connectivity checks | Correct supplies and connections, required PG DRC/connectivity clean |
| Placement | place_opt, legality/congestion/timing | Legal placement, acceptable congestion/density and complete reports/checkpoint |
| CTS | Qualified clock setup, clock_opt, clock QoR and timing | Clock connectivity, required skew/insertion delay and setup/hold analysis |
| Routing | route_auto/route_opt and route checks | Completed nets; required DRC/antenna/connectivity; new checkpoint/netlist |
| Extraction | StarRC qualified recipe or approved supported equivalent | Complete parasitics per RC corner, no unresolved required opens/shorts, mapping provenance |
| Signoff timing | PrimeTime netlist+SDC+parasitics per mode/corner | Setup/hold/recovery/removal closure, annotation/analysis coverage, no unexplained unconstrained paths |
| Physical signoff | Qualified ICV DRC/LVS/antenna and connectivity; IR/EM if required and supported | Complete zero-unwaived results, correct deck/process/top/netlist/layout revisions |
| Stream and final verification | write_gds with qualified layer map and cell GDS; reverify final stream | Correct top/cells/layers, stream integrity, final-stream DRC/LVS/antenna and all required objectives |

The manifest runner splits these into `rtl`, `constraints`, `synthesis`, `formal`,
`floorplan`, `power`, `placement`, `cts`, `routing`, `extraction`, `timing`,
`physical`, `streamout`. Full mode requires the complete ordered chain.
Use `--partial` for explicitly scoped stage experiments; its result can only say
`partial-stage-validated`, never end-to-end. A logical ECO during physical work
adds a new equivalence gate before promotion and invalidates extraction/signoff;
the agent must insert that verification into its reviewed stage adapter, with
an additional required check such as `eco_equivalence`, and retain its report.

## Execute and recover

Generate design-specific copies of [Tcl templates](../../templates) using the
actual PDK inputs, with validated command options and meaningful report/query
checks. Templates that omit result.json intentionally require a PDK/report adapter:
add that adapter before running them in an autonomous promotion chain. A marker,
empty report or unconditional Boolean is not a physical verification evaluator.

```sh
python3 scripts/flow.py preflight /absolute/design.manifest.json
python3 scripts/flow.py run /absolute/design.manifest.json --out /absolute/runs/design/run-001
```

On failure, preserve command/status/console/internal logs and reports; classify
with [troubleshooting](../synopsys-troubleshooting/SKILL.md). Inspect the current
state and installed command/diagnostic manual. Correct the smallest demonstrated
cause. Recover missing inputs/environment/command syntax by fixing that cause;
do not tune utilization to address a license failure. For a design tradeoff,
record old/new values and metric hypothesis, restore the last valid incoming
checkpoint into a new writable copy, run the affected stages and compare.
Keep or revert based on verification and measured improvement, retaining both.

Use [optimization](../synopsys-optimization/SKILL.md) for bounded PPA trials.
Never change original RTL behavior, remove modules/constraints, relax hard targets
or disable required verification to make a run pass. Explain necessary functional
changes and obtain the user's authorization first. Retry only within the attempt,
license, wall-time and no-improvement budgets. On exhaustion, report the genuine
blocker, exact evidence and next required input/action.

## Final result

Return absolute artifact/report/checkpoint paths, input/tool/deck versions and
hashes, stage/iteration history, accepted/reverted changes, achieved metrics and
units, proof/coverage/signoff results, blockers and reproducible next commands.
Separate `GDS generated` from `final stream verified` and `objectives met`.
State the highest earned evidence level. Read [validation scope](../../READINESS.md) and establish local tool, stage and end-to-end evidence for the current design.
