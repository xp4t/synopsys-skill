---
name: synopsys-design-compiler
description: "Use when operating Design Compiler or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# Design Compiler

## Purpose and configuration

Elaborate RTL, map logic to characterized standard cells, optimize timing/area/power and export implementation netlists. DC output is a logical implementation; it is not a physical or signoff result.

Resolve `dc_shell` from the user's configured environment or tool profile.
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
dc_shell -f design.tcl
```

For supported stage scripts, [flow.py](../../scripts/flow.py) captures commands,
status, logs, artifacts and checkpoints without requiring a shell wrapper.
Tools may provide native interfaces with different semantics for similar flags.

## Inputs and outputs

Ordered Verilog/SystemVerilog/VHDL sources, top, parameters/defines/include paths, target/link .db libraries, approved SDC; UPF and physical references when required. Record reset semantics and DesignWare dependencies. `.lib` conversion requires a working Library Compiler; verify its availability locally.

Mapped .v, .ddc, exported .sdc, synthesis .svf; design, constraint, area, timing, power and QoR reports. Retain unmapped/elaboration evidence and the original RTL/SDC hashes. Tutorial library area is in library units, not an asserted square-micron value.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| RTL | `analyze elaborate link check_design` | Logical libraries and ordered sources must resolve every required reference. |
| Constraints | `read_sdc check_timing report_clock` | Inspect clock definitions, all interface delays, recovery/removal, exceptions and unconstrained endpoints. |
| Mapping | `compile compile_ultra` | Use compile -map_effort medium/high; compile_ultra needs its feature license and mode prerequisites. |
| Inspection | `report_area report_timing report_power report_qor` | Read units, activity assumptions and path coverage; power is an estimate without appropriate activity. |
| Export | `set_svf write_file write_sdc` | Enable SVF before transformations; emit mapped netlist and checkpoint together. |

## Tcl, inspection and documentation

current_design; get_designs *; get_cells -hierarchical; get_clocks *; report_hierarchy; check_design; check_timing. Check sizeof_collection, not Tcl llength, for Synopsys collections.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool design-compiler --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

Map effort (medium/high), incremental compile, buffering/cell choices permitted by the PDK, area versus timing emphasis. compile_ultra -timing_high_effort_script and -area_high_effort_script are distinct strategies; retrieve restrictions before combining switches. Retime, hierarchy changes and clock gating change verification obligations and require new equivalence evidence.

Lower area can increase delay and fanout. Physical-aware/topographical settings require physical libraries and RC technology; never enable them just because their flags exist. Clock period and interface budgets remain fixed. A changed netlist invalidates Formality and all downstream checkpoints.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Diagnose source order, defines, unresolved references, library selection and constraints before tuning. Review inferred latches and multiple drivers against functional intent. Unsupported commands need installed-version documentation. License or loader failures need environment repair.

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

- [templates/rtl-check.tcl](../../templates/rtl-check.tcl)
- [templates/dc-synthesis.tcl](../../templates/dc-synthesis.tcl)

Inspect the actual outputs and product-specific reports against the requested
scope. For synthesis/implementation, require mapped/linked artifacts and preserved
constraints; reprove functionality after transformations. For verification,
require complete coverage and clean required checks. For simulation/debug,
require the intended task/test to complete with reviewed diagnostics.

Keep documentation validation, Tcl syntax checks, tool execution, stage acceptance
and end-to-end signoff evidence separate. A generated stream is not a verified
implementation. See [execution contract](../../references/execution-contract.md)
and [validation scope](../../READINESS.md) for the required evidence boundaries.
