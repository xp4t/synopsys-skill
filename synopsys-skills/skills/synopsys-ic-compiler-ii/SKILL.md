---
name: synopsys-ic-compiler-ii
description: "Use when operating IC Compiler II or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# IC Compiler II

## Purpose and configuration

NDM-based digital physical implementation from a mapped netlist through floorplan, power, placement, CTS, routing and stream-out. Library Manager is a separate shell, covered by synopsys-ndm-library-manager.

Resolve `icc2_shell` from the user's configured environment or tool profile.
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
icc2_shell -file design.tcl
```

For supported stage scripts, [flow.py](../../scripts/flow.py) captures commands,
status, logs, artifacts and checkpoints without requiring a shell wrapper.
Tools may provide native interfaces with different semantics for similar flags.

## Inputs and outputs

Mapped equivalent netlist; technology .tf or technology NDM; compatible cell/macro NDMs, site/row definitions, SDC/MCMM scenarios, RC corners and layer maps; qualified power-grid recipe, cell GDS and signoff decks. Logical .db alone cannot supply placement/routing geometry.

Versioned design.ndm checkpoints with block labels; congestion, legality, timing, clock, PG and route reports; post-route netlist/SDC/parasitics and final GDS. Save the whole NDM library and dependencies, not only a block-name string.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Initialize | `create_lib read_verilog link_block read_sdc` | create_lib -technology and -ref_libs; read_verilog -top; verify technology units and references. |
| Floorplan | `initialize_floorplan create_placement_blockage create_keepout_margin` | Set core utilization/offset or explicit dimensions. Check rows, macros, IO, halos and legal sites. |
| Power | `create_pg_ring_pattern create_pg_mesh_pattern set_pg_strategy compile_pg connect_pg_net check_pg_connectivity check_pg_drc` | Use foundry-reviewed nets, layer widths/pitches/vias; no generic universal PDN. |
| Placement | `place_opt check_legality report_congestion` | Start from a valid floorplan+PG checkpoint; assess local congestion, pin access and timing by scenario. |
| CTS | `clock_opt report_clock_qor report_timing` | Clock definitions, reference cells, routing rules and skew budgets must be established first. |
| Route | `route_auto route_opt check_routes` | Check unrouted nets, route DRC, antenna and setup/hold, then revalidate any logic ECO. |
| Export | `write_verilog write_sdc write_parasitics write_gds save_block save_lib` | RC/export syntax is tool-specific. GDS uses -layer_map and -merge_files for qualified cell views. |

## Tcl, inspection and documentation

current_block; get_blocks *; get_libs *; get_cells *; get_clocks *; get_scenarios *; report_qor; report_timing; report_congestion; report_clock_qor. get_app_options and report_app_options expose version-specific options; read man before changing one.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool ic-compiler-ii --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

Core utilization within the approved die/area envelope; placement/congestion app options only after retrieving their installed defaults and restrictions; clock reference/routing settings and route effort when supported. Use get_app_option_value/report_app_options to capture original values; set_app_options changes state.

Density affects wirelength, pin access, routing capacity and area. Macro placement and PG straps constrain routing resources. CTS changes insertion delay/skew and both setup/hold. A floorplan change invalidates every later block; a route ECO invalidates extraction, timing, formal where logical, and physical signoff.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Separate technology/site/schema mismatch from density, pin access and routing congestion. Check PG and clock connectivity before effort tuning. Inspect per-scenario setup/hold and required physical rules. Never ignore required DRC to claim a pass.

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

- [templates/icc2-floorplan.tcl](../../templates/icc2-floorplan.tcl)
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
