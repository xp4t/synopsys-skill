---
name: synopsys-primetime
description: "Use when operating PrimeTime or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# PrimeTime

## Purpose and configuration

Static timing and, with licensed features and valid activity/models, power and signal-integrity analysis. It verifies implemented netlists and parasitics against the approved timing specification.

Resolve `pt_shell` from the user's configured environment or tool profile.
Discover the actual release, supported options, licenses and documentation locally.
Use [environment discovery](../synopsys-environment/SKILL.md); do not assume a
particular installation directory, account, license endpoint or startup shell.
Keep installation inventories, logs and documentation indices in private local state.

## Invocation and command conventions

Use the configured executable directly from the prepared environment. Preserve
its wrapper filename; changing a dispatcher's invocation name can select a different
product. Confirm interactive and batch conventions in that release's documentation.
This reference provides command candidates, not proof they exist in every release.

```text
pt_shell -file design.tcl
```

For supported stage scripts, [flow.py](../../scripts/flow.py) captures commands,
status, logs, artifacts and checkpoints without requiring a shell wrapper.
Tools may provide native interfaces with different semantics for similar flags.

## Inputs and outputs

Signoff netlist, compatible timing .db files for each PVT/RC corner, original approved SDC, complete SPEF/GPD with name mapping, operating conditions and derates; activity/UPF/SI models when required. For .lib conversion, restore the missing Library Compiler instead of inventing its path.

Per-mode/corner setup, hold, recovery/removal, clock and exception reports; annotation and analysis coverage; unconstrained endpoint diagnostics and power/SI reports where applicable. Include units and model provenance.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Load | `read_db read_verilog link_design read_sdc` | Resolve every reference and validate clocks/IO delays; distinguish black boxes from permitted abstractions. |
| Parasitics | `read_parasitics report_annotated_parasitics` | Verify extraction corner, coupling policy and annotation coverage, not merely successful read. |
| Analysis | `update_timing check_timing report_analysis_coverage report_timing` | Run max/setup and min/hold at every required corner; inspect untested and unconstrained paths. |
| Optional power/SI | `report_power report_noise` | Feature/license/model prerequisites apply. Never infer IR/EM closure from STA. |

## Tcl, inspection and documentation

current_design; get_libs *; get_clocks *; get_cells -hierarchical; report_units; report_clock; report_constraint; report_timing; check_timing; report_analysis_coverage.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool primetime --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

Analysis effort/PBA reporting and ECO suggestions supported by this release. SI enablement, derates, coupling reduction and clock propagation are methodology settings with correctness implications, not free PPA knobs. Keep qualified signoff settings pinned.

Netlist, library corner, SDC and SPEF names/corners must agree. Missing parasitics can make timing optimistic. Setup and hold require different corners and min/max path analysis. Clock uncertainty and false/multicycle paths come from requirements and verified exceptions.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Check library and parasitic annotation, clocks, interface delays, corner consistency and analysis coverage. Diagnose any library-compiler dependency using the installed message manual and actual input format. Never hide unconstrained paths or change exceptions to remove violations.

Capture the command/status, internal logs, reports and state/checkpoint identity.
Classify the cause, consult the relevant installed documentation and apply the
least disruptive justified correction. Restore a writable copy of the last valid
incoming checkpoint and rerun affected stages. Compare verified metrics before
keeping a change; retain rejected attempts. Use
[troubleshooting](../synopsys-troubleshooting/SKILL.md) for the recovery decision.

Functional changes need explicit authorization. Do not relax timing requirements,
remove required constraints or bypass verification to report success. Stop when
no justified correction remains or a configured budget is exhausted, and report
what input or environment repair is needed.

## Templates and acceptance

- [templates/primetime.tcl](../../templates/primetime.tcl)

Inspect the actual outputs and product-specific reports against the requested
scope. For synthesis/implementation, require mapped/linked artifacts and preserved
constraints; reprove functionality after transformations. For verification,
require complete coverage and clean required checks. For simulation/debug,
require the intended task/test to complete with reviewed diagnostics.

Keep documentation validation, Tcl syntax checks, tool execution, stage acceptance
and end-to-end signoff evidence separate. A generated stream is not a verified
implementation. See [execution contract](../../references/execution-contract.md)
and [validation scope](../../READINESS.md) for the required evidence boundaries.
