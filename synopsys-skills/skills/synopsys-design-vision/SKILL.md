---
name: synopsys-design-vision
description: "Use when operating Design Vision or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# Design Vision

## Purpose and configuration

DC graphical design inspection and synthesis interaction. Use Design Compiler for reproducible headless synthesis; Design Vision is useful for hierarchy, timing and schematic investigation.

Resolve `design_vision` from the user's configured environment or tool profile.
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
design_vision -f design.tcl
```

For supported stage scripts, [flow.py](../../scripts/flow.py) captures commands,
status, logs, artifacts and checkpoints without requiring a shell wrapper.
Tools may provide native interfaces with different semantics for similar flags.

## Inputs and outputs

DC .ddc or supported RTL/netlist with matching libraries, SDC and design setup; a working display for GUI use. Use copies of checkpoints for exploratory editing.

DC-compatible design checkpoints, reports and session logs; explicitly exported GUI artifacts when supported. Do not overwrite accepted synthesis checkpoints while inspecting.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Load/inspect | `read_ddc current_design report_hierarchy report_timing` | Use synthesis library/constraint context matching the saved design. |
| Synthesis | `analyze elaborate compile` | Delegate reproducible synthesis and formal gates to synopsys-design-compiler. |
| Save | `write_file write_sdc` | Treat any design modification as a new candidate requiring verification. |

## Tcl, inspection and documentation

DC design/collection commands apply where documented: current_design, get_designs *, report_hierarchy, report_timing, report_area and check_design. GUI-specific APIs must be looked up separately.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool design-vision --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

Synthesis settings follow DC policy. GUI display/layout settings are observational; any mapped design edit invalidates downstream equivalence and physical evidence.

Same DC release/database/library context; GUI libraries/display can fail independently of dc_shell. Use exact wrapper name because it selects the product personality.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Diagnose display/GUI setup separately from synthesis errors. Preserve wrapper names and design/library context. Any design edit requires new synthesis/formal evidence before downstream promotion.

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
