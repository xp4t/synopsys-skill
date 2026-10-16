---
name: synopsys-starrc
description: "Use when operating StarRC or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# StarRC

## Purpose and configuration

Extract interconnect parasitics using qualified technology and layout/connectivity data; hand parasitics to STA. StarXtract extraction controls are not an ICC2 Tcl script.

Resolve `StarXtract` from the user's configured environment or tool profile.
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
Use the documented native driver procedure in the table below.
```

For supported stage scripts, [flow.py](../../scripts/flow.py) captures commands,
status, logs, artifacts and checkpoints without requiring a shell wrapper.
Tools may provide native interfaces with different semantics for similar flags.

## Inputs and outputs

Qualified extraction command file/recipe, NDM/Milkyway/GDS/OA handoff supported by the licensed mode, netlist/connectivity, layer mapping, RC technology model, required corners and extraction scope. The installed command-file parameter reference is incomplete; obtain the PDK-qualified recipe/manual before constructing extraction controls.

Extraction transcript, RC error/open/short reports, extracted SPEF/GPD/DSPF as specified by the reviewed recipe, model/corner provenance and annotation checks in the consuming STA tool.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Driver inspection | `StarXtract -h; StarXtract -v` | Recorded usage exposes supported invocation flags; return status differs from actual extraction success. |
| Diagnostic documentation | `starrc_man SX-message_number` | Use a real message code from the log. starrc_man accepts diagnostic codes, not -help. |
| Constraints Tcl | `starrc_shell -no_init -file constraints.tcl` | This companion is a PrimeTime-related constraint interface; it is not proof that StarXtract accepts Tcl. |
| Integrity utility | `StarXtract -gdscheck layout.gds` | Flag is in installed usage. Inspect actual result; structural checking does not replace DRC/LVS. |

## Tcl, inspection and documentation

Inspect model/corner/version headers, extracted net counts, shorts/opens and output parasitics. In starrc_shell use info commands and help/man; its live registry is separate from extraction control keywords.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool starrc --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

Extraction accuracy/distribution/scope only within a qualified methodology and documented controls. Never discard coupling or skip nets to improve reported timing. Corner/model changes require rerunning STA and consistent naming/units.

Layer map, geometry database, RC model and PVT/RC corner must be compatible. Post-route ECO invalidates parasitics. A valid parasitic file with low annotation coverage cannot support timing closure.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Check extraction technology, layer maps, layout/connectivity handoff and required corners. Read the exact diagnostic message documentation. Do not substitute utility-shell commands or invent extraction control keywords when the required reference is unavailable.

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
