---
name: synopsys-vc-static
description: "Use when operating Embedded VC Static or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# Embedded VC Static

## Purpose and configuration

Embedded static/formal-analysis support distributed with VCS. It must not be mistaken for an installed, working standalone SpyGlass product or a substitute for proven lint/CDC flows.

Resolve `vc_static_shell` from the user's configured environment or tool profile.
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
vc_static_shell -file design.tcl
```

For supported stage scripts, [flow.py](../../scripts/flow.py) captures commands,
status, logs, artifacts and checkpoints without requiring a shell wrapper.
Tools may provide native interfaces with different semantics for similar flags.

## Inputs and outputs

A complete compatible VC Static image, appropriate feature licenses and a documented RTL/static-analysis methodology. Source/top/defines/clocks and analysis goals must be explicit.

Tool sessions, analysis reports, proof/coverage diagnostics when a complete image is restored. Current outputs are help and missing-executable logs only.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Driver help | `vc_static_shell -help` | Requires VC_STATIC_HOME; help lists -batch, -file/-f, -no_init and session switches. |
| Tcl startup | `vc_static_shell -no_init -batch -file script.tcl` | Validate startup and analysis capabilities against the configured installation. |

## Tcl, inspection and documentation

After installation repair, enumerate info commands and help/man if supported. Use embedded VCS static-analysis manuals and explicit checks for each feature; do not copy SpyGlass APIs.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool vc-static --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

No operational tuning is authorized by current evidence. Once repaired, use methodology-specific documented proof/lint effort and resource bounds; never hide required checks or waive errors to finish.

VC_STATIC_HOME, complete architecture image, feature license and matching VCS release. A wrapper/help response does not establish a working analysis engine.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Verify that the complete analysis image and required licenses are available. A wrapper help response is not an executed lint/formal workflow. Retrieve product-specific analysis APIs rather than assuming another static-analysis product has the same commands.

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
