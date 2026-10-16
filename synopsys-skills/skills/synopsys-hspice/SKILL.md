---
name: synopsys-hspice
description: "Use when operating PrimeSim HSPICE or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# PrimeSim HSPICE

## Purpose and configuration

Circuit-level SPICE analysis for transistor/analog verification and characterization. It supports electrical simulation, not RTL synthesis or automatic digital physical implementation.

Resolve `hspice` from the user's configured environment or tool profile.
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

SPICE netlist/deck with analysis directives, approved model libraries/corners, supplies, temperatures and measurements. Include paths and model revisions must be explicit. The bundled RC example uses ideal components only.

Listing .lis, status/log files, waveform/measurement files according to analysis/output options. Check convergence and completion in .lis as well as process status; preserve all run prefixes.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Usage | `hspice -h` | Lists input/output and threading switches. |
| Circuit simulation | `hspice -i circuit.sp -o result_prefix` | Input deck selects .op/.dc/.ac/.tran and measurements. |
| Inspect | `Read result_prefix.lis and measurement/waveform files` | Check job conclusion, convergence, expected analyses and measurement validity. |

## Tcl, inspection and documentation

Read listing model/corner headers, node/device summaries, convergence diagnostics and measurement results. SPICE directives and CLI switches are not Synopsys Tcl commands.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool hspice --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

Supported solver accuracy/convergence and threading settings only after reading their defaults/restrictions in primesim_continuum_cmdref. Looser tolerances can change result accuracy; they cannot be used to claim a previously failing electrical spec passed.

Models, units, temperature, supplies, timestep and convergence affect measurement comparability. Thread count can affect resource use; verify reproducibility. Supply/temperature/model-corner changes are specification changes, not generic optimization.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Separate missing models/includes, invalid netlists, convergence and failed measurements. Review operating conditions and model validity before changing solver controls. Retain the full listing and undefined-measurement diagnostics.

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
