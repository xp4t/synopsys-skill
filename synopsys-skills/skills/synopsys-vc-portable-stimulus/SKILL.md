---
name: synopsys-vc-portable-stimulus
description: "Use when operating VC Portable Stimulus or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# VC Portable Stimulus

## Purpose and configuration

Compile Portable Stimulus models, solve scenarios and map generated tests to supported execution targets. This is optional functional-verification infrastructure, not a physical implementation stage.

Resolve `vcps` from the user's configured environment or tool profile.
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

PSS source/filelist, root action, solver constraints, target mapping/executor definitions and reproducible random seed. Keep generated stimulus paired with the tested design/specification.

snps_vcps_dir or explicitly selected -vcps_dir, compile/solve/mapping outputs and generated C/SystemVerilog target tests and coverage when requested.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Help | `vcps -help` | Needs VCPS_HOME, unlike VCS_HOME used by the simulator. |
| Compile | `vcps -compile model.pss` | Installed help documents -f, -incdir and -vcps_dir. |
| Solve | `vcps -solve -root_action action_type -num_cases N -random_seed seed` | Choose values from the user verification plan; bound solve CPU/time. |
| Map | `vcps -map` | Retrieve target/executor options from captured usage before generating a runnable test. |

## Tcl, inspection and documentation

Inspect driver help and compile/solver diagnostics, root-action selection, number of generated scenarios and seed. Local doc/pss_examples supplies worked source examples; there is no proven general Tcl shell for this driver.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool vc-portable-stimulus --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

Solver seed/case count/CPU limits and target mapping controls documented in the installed help. A smaller coverage set cannot replace the requested verification scope. Retain failing/unsatisfiable cases.

PSS model constraints, executor mapping, target language, simulator/compiler environment and verification objectives must align. Generated tests still need execution and result checking.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Diagnose model constraints, root action, executor mapping, compiler/solver availability and licenses. Preserve unsatisfiable and failing cases. Reducing test scope or deleting constraints is not a substitute for verification.

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
