---
name: synopsys-ndm-library-manager
description: "Use when operating NDM Library Manager or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# NDM Library Manager

## Purpose and configuration

Prepare and validate NDM reference libraries for ICC2/Fusion using technology, logical timing and physical cell views. It is distinct from the missing standalone Liberty Library Compiler.

Resolve `icc2_lm_shell` from the user's configured environment or tool profile.
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
icc2_lm_shell -file design.tcl
```

For supported stage scripts, [flow.py](../../scripts/flow.py) captures commands,
status, logs, artifacts and checkpoints without requiring a shell wrapper.
Tools may provide native interfaces with different semantics for similar flags.

## Inputs and outputs

Technology/site/layer definitions, logical .db timing views and matching LEF/physical inputs, cell naming/units and required corners. A set of unrelated sample .db/.tf files is not a coherent reference library.

Workspace diagnostics and committed reference NDM libraries, with complete input/view/corner provenance. Keep original qualified reference libraries read-only.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Workspace | `create_workspace` | Retrieve the installed flow/technology options; choose a flow appropriate to supplied views. |
| Read/check | `read_db read_lef check_workspace` | Validate cell/view consistency, sites, layers, units and timing corners before commit. |
| Commit | `commit_workspace` | Write a new output library, then verify it loads into the intended implementation release. |

## Tcl, inspection and documentation

get_libs *; info commands; help -groups; help -verbose create_workspace; man create_workspace; man check_workspace. Query workspace state using the installed LM reference.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool ndm-library-manager --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

View inclusion and documented workspace options within the foundry methodology. Removing pins/cells/corners or ignoring consistency errors is not a PPA optimization.

Logical and physical cell names, units, pin geometry, sites, layers and PVT corners must agree. Rebuilding a reference invalidates downstream technology-link assumptions and physical results.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Resolve cell/view, pin, site, layer, unit and corner mismatches before committing references. Verify logical-library conversion capability separately; reference-library management is not proof that every Liberty conversion feature is available.

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
