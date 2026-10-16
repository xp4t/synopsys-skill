---
name: synopsys-verdi
description: "Use when operating Verdi or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# Verdi

## Purpose and configuration

Debug RTL/netlists and simulation waveforms, inspect hierarchy and automate supported GUI/debug operations through its Tcl command API. It does not place, route or establish signoff.

Resolve `verdi` from the user's configured environment or tool profile.
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
verdi -batch -play debug.tcl
```

For supported stage scripts, [flow.py](../../scripts/flow.py) captures commands,
status, logs, artifacts and checkpoints without requiring a shell wrapper.
Tools may provide native interfaces with different semantics for similar flags.

## Inputs and outputs

RTL/netlist filelist and matching compilation database, FSDB/VPD or other supported waveform data, include/define settings and debug symbols. GUI use also requires a valid display; batch -play can run without it.

verdiLog directory, command history/playback scripts, loaded-debug metadata, waveforms/screenshots/reports from explicitly selected API commands. Preserve source/waveform revision pairing.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Invocation | `verdi -help` | Lists driver switches and batch/playback behavior. |
| Batch Tcl | `verdi -batch -play script.tcl` | Use Tcl info commands/namespace inspection; retrieve GUI Tcl API documentation before API calls. |
| Debug inputs | `verdi -f sources.f -ssf waves.fsdb` | Filelist and dump must correspond to the same compiled design revision. |

## Tcl, inspection and documentation

Tcl: puts [info patchlevel]; puts [lsort [info commands]]; namespace children ::. Then look up the needed API in share/libcmd/doc/tcl.pdf or doc/.verdi_tcl.txt.gz if present. Do not assume help/man from implementation shells exists.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool verdi --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

Waveform signal selection, debug scope and batch report capture. Reducing dumps can save disk/runtime but must retain signals needed for the failing assertion or compare point. Instrumentation changes require a fresh matching simulation.

Version-compatible FSDB/PLI/debug databases, design hierarchy and compile options must align. GUI display and license-tier fallback can affect startup. A failed playback command can leave the app running, so bound every batch process.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Use the application-specific command API rather than assuming implementation-shell help commands. Match waveforms/debug databases to the exact design revision. Bound batch playback because a failed command can leave an application running.

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
