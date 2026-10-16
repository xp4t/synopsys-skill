---
name: synopsys-fusion-compiler
description: "Use when operating Fusion Compiler or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# Fusion Compiler

## Purpose and configuration

Integrate physically aware synthesis and digital implementation in an NDM flow. It can substitute for DC plus parts of ICC2 when a compatible Fusion technology/reference-library setup exists.

Resolve `fc_shell` from the user's configured environment or tool profile.
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
fc_shell -file design.tcl
```

For supported stage scripts, [flow.py](../../scripts/flow.py) captures commands,
status, logs, artifacts and checkpoints without requiring a shell wrapper.
Tools may provide native interfaces with different semantics for similar flags.

## Inputs and outputs

Original RTL/top/defines, approved SDC, qualified NDM technology and physical/logical cell references, MCMM corners, UPF where required, power/clock/routing recipes. Do not substitute DC target_library-only initialization for Fusion initialization.

Fusion design library, labeled blocks and transformed netlists; QoR/timing/congestion/clock/route reports; SVF/verification handoff where configured; post-route netlist, parasitics and GDS.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Initialize | `create_lib read_verilog link_block read_sdc` | Use a qualified Fusion init recipe to establish logical and physical references and scenarios. |
| Synthesis | `compile_fusion` | -check_only checks prerequisites. -list_only enumerates stages. Read allowed -from/-to stage values before restarting. |
| Implementation | `place_opt clock_opt route_auto route_opt` | Only resume at valid boundaries supported by this version and the saved block state. |
| Queries/export | `report_qor report_timing report_congestion save_block save_lib write_gds` | Read ICC2 shared manuals only when applicable to the live Fusion command registry. |

## Tcl, inspection and documentation

current_block; get_scenarios *; get_clocks *; report_qor; report_timing; report_congestion; report_clock_qor; report_app_options. Use compile_fusion -list_only to inspect implementation boundaries before selecting a restart.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool fusion-compiler --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

Documented synthesis/placement/congestion effort options, authorized utilization and clock/routing options. Snapshot all option values. Prefer one bounded hypothesis per experiment. Avoid copied DC-only compile switches.

Fusion optimization stages span logical and physical transformations. A changed stage boundary can invalidate downstream assumptions and formal mapping. Original RTL remains the functional reference, even when physical optimizations rewrite logic.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Validate NDM references, logical models, scenarios and supported compile boundaries. Diagnose command/mode/license errors separately from timing and congestion. Preserve the accepted block when testing a new strategy.

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

- [templates/fc-synthesis.tcl](../../templates/fc-synthesis.tcl)
- [templates/icc2-implement.tcl](../../templates/icc2-implement.tcl)
- [templates/streamout.tcl](../../templates/streamout.tcl)

Inspect the actual outputs and product-specific reports against the requested
scope. For synthesis/implementation, require mapped/linked artifacts and preserved
constraints; reprove functionality after transformations. For verification,
require complete coverage and clean required checks. For simulation/debug,
require the intended task/test to complete with reviewed diagnostics.

Keep documentation validation, Tcl syntax checks, tool execution, stage acceptance
and end-to-end signoff evidence separate. A generated stream is not a verified
implementation. See [execution contract](../../references/execution-contract.md)
and [validation scope](../../READINESS.md) for the required evidence boundaries.
