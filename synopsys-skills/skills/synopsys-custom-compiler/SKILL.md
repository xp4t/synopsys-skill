---
name: synopsys-custom-compiler
description: "Use when operating Custom Compiler or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# Custom Compiler

## Purpose and configuration

Custom schematic/layout editing and supported analog/custom design automation. It is not an interchangeable RTL-to-GDS digital implementation engine.

Resolve `custom_compiler` from the user's configured environment or tool profile.
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

Qualified OpenAccess PDK/library definitions, cell/view/top selection and relevant schematic/layout/netlisting/simulation configuration; display configuration for GUI operations. Back up custom design views before edits.

OA cell/view databases, netlists, application logs and reports/stream files from requested operations. Capture changed library/cell/view identities and use a writable isolated copy.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Wrapper inspection | `custom_compiler --wrapper-help` | This switch is in the installed wrapper; application startup remains blocked. |
| Tcl discovery | `info commands; namespace children ::` | After environment repair, enumerate APIs and retrieve cc_tclref.pdf before invoking namespace commands. |
| Custom flow | `Use local cc_getting_started/cc_leuser/cc_seuser/cc_tclref procedures` | Document required OA/PDK semantics and checkpoints; no generic ICC2 Tcl substitutions. |

## Tcl, inspection and documentation

Inspect supported Tcl namespaces and the installed Tcl/Python and OA/technology references for release-specific object/session queries. Do not fabricate namespace APIs from memory.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool custom-compiler --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

Only documented editor/netlisting/simulation settings with a concrete task and valid PDK. Layout devices, connectivity and schematic parameters are functional/electrical design choices; require appropriate authorization and verification.

OA schema, PDK technology, device callbacks, Python/Tcl ABI and host shared libraries must agree. Digital NDM and custom OA references are distinct; use documented interoperability procedures.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Diagnose application loader, OA/PDK and API compatibility separately from cell/view problems. Preserve source views and use a writable design copy. Do not change system libraries or global environment settings as an automatic workaround.

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
