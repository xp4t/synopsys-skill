---
name: synopsys-ic-compiler
description: "Use when operating IC Compiler (legacy) or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# IC Compiler (legacy)

## Purpose and configuration

Legacy Milkyway-based digital implementation. Keep its technology, database and Tcl APIs separate from NDM-based ICC2/Fusion flows.

Resolve `icc_shell` from the user's configured environment or tool profile.
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
icc_shell -f design.tcl
```

For supported stage scripts, [flow.py](../../scripts/flow.py) captures commands,
status, logs, artifacts and checkpoints without requiring a shell wrapper.
Tools may provide native interfaces with different semantics for similar flags.

## Inputs and outputs

Compatible Milkyway technology/reference libraries, mapped netlist, SDC, RC tables and qualified legacy floorplan/PG/clock/route recipes. An NDM library cannot be assumed interchangeable.

Milkyway design/cell checkpoints, implementation reports and stream-out files when a working environment and PDK are available. No legacy design stage has executed here.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Initialize | `create_mw_lib open_mw_lib read_verilog link` | Use installed ICC manuals and qualified legacy references, not create_lib NDM recipes. |
| Floorplan/place | `create_floorplan place_opt` | Validate actual legacy command options and technology prerequisites. |
| CTS/route | `clock_opt route_opt` | Restore a valid Milkyway checkpoint and inspect the stage-specific reports. |
| Inspect/save | `report_timing report_qor save_mw_cel` | Do not confuse a Milkyway cell with an ICC2 block label. |

## Tcl, inspection and documentation

Use current_design, report_qor, report_timing and check_design where supported; inspect legacy library/cell state through the installed APIs and verify current command availability.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool ic-compiler --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

Only legacy ICC options documented for the installed release and the qualified technology. Density, clock and routing settings are subject to the same immutable functional/timing requirements as ICC2.

Milkyway database compatibility and legacy RC/technology setup govern restarts. Migrating to ICC2 requires a reviewed handoff; choosing a different tool does not automatically convert databases or signoff methodology.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Validate legacy database and technology compatibility. Do not apply NDM commands or assume automatic conversion from another implementation system. Diagnose loader or license failures before attempting design recovery.

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

Use the product-native procedure in the table. This driver may use filelists, SPICE, PSS or verification runsets rather than implementation Tcl.

Inspect the actual outputs and product-specific reports against the requested
scope. For synthesis/implementation, require mapped/linked artifacts and preserved
constraints; reprove functionality after transformations. For verification,
require complete coverage and clean required checks. For simulation/debug,
require the intended task/test to complete with reviewed diagnostics.

Keep documentation validation, Tcl syntax checks, tool execution, stage acceptance
and end-to-end signoff evidence separate. A generated stream is not a verified
implementation. See [execution contract](../../references/execution-contract.md)
and [validation scope](../../READINESS.md) for the required evidence boundaries.
