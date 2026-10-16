---
name: synopsys-vcs
description: "Use when operating VCS or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# VCS

## Purpose and configuration

Compile/elaborate and simulate Verilog/SystemVerilog/VHDL testbenches; establish a regression baseline before synthesis. Simulation tests observed cases and complements formal equivalence.

Resolve `vcs` from the user's configured environment or tool profile.
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

RTL and testbench filelists, source language switches, defines/include directories, top configurations, DPI/PLI libraries and compiler toolchain. Use PDK simulation models for gate-level simulations, plus SDF when timing simulation is requested.

Compile transcript, simv executable and its simv.daidir/runtime dependencies, simulation logs, VPD/FSDB/VCD and coverage databases when enabled. Keep compiler output directories together; the executable alone may not be portable.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Compiler help | `vcs -help; vcs -ID` | Verify the installed driver and architecture image before compiling. |
| Compile | `vcs -full64 -sverilog -o simv rtl.sv tb.sv` | Use the configured executable and VCS_HOME matching that exact image. |
| Simulate | `./simv` | Require testbench assertions, expected completion marker and no errors; timeout incomplete tests. |
| Debug | `vlogan; vhdlan; verdi` | Multi-step/mixed-language compilation needs documented library mappings. Load waveforms with the Verdi skill. |

## Tcl, inspection and documentation

Inspect compile/elaboration diagnostics, detected tops, simv runtime banner, assertion summaries and explicit regression markers. There is no DC-style current_design query in the compiler driver.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool vcs --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

Compile/debug/coverage settings and explicit simulation seeds. Simulation seed is a reproducibility parameter, not permission to select only passing seeds. Runtime step/time limits must still complete required tests. Optimization flags require installed help evidence.

VCS_HOME, architecture kernel, C/C++ ABI, DPI/PLI and simulator runtime must match. Debug/coverage instrumentation trades runtime/memory for visibility; changing it must preserve test semantics and required coverage.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Check the selected executable, matching installation environment, architecture image, filelist and language options. Preserve assertion failures, seeds and waves. A compiler ID banner does not prove simulation can execute.

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
