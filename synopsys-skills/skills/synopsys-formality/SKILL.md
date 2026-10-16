---
name: synopsys-formality
description: "Use when operating Formality or diagnosing its release-specific commands, inputs, results, or startup requirements."
---

# Formality

## Purpose and configuration

Compare original RTL against synthesized or transformed implementations. Equivalence failure, aborted proofs or unjustified black boxes block promotion of that implementation.

Resolve `fm_shell` from the user's configured environment or tool profile.
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
fm_shell -file design.tcl
```

For supported stage scripts, [flow.py](../../scripts/flow.py) captures commands,
status, logs, artifacts and checkpoints without requiring a shell wrapper.
Tools may provide native interfaces with different semantics for similar flags.

## Inputs and outputs

Immutable reference RTL, exact mapped/ECO netlist, shared technology .db files, synthesis SVF, matching defines/parameters and explicit setup assumptions. Preserve reference/implementation identity and source hashes.

Verification transcript, passing/failing/unmatched/aborted point reports, constants/dont-verify/black-box reports, auto-setup summary and .fss session for diagnosis.

## Stage operations

Retrieve the installed command syntax, argument types, defaults, restrictions,
examples, feature requirements and design-state prerequisites before constructing
new commands. Identify whether each operation queries state, updates derived state,
mutates a design or exports artifacts.

| Stage | Commands or native procedure | Prerequisites and checks |
| --- | --- | --- |
| Setup | `set_svf read_db` | Set SVF before reading designs. Plain read_db loads shared libraries into existing and future containers. |
| Reference/implementation | `read_verilog read_sverilog read_vhdl set_top` | Use explicit -r and -i containers for designs; choose parser from the actual source language. |
| Compare | `match verify` | Capture verify return value. Unresolved references and missing tops must stop the script immediately. |
| Inspect/restart | `report_failing_points report_unmatched_points report_aborted_points report_black_boxes report_dont_verify_points report_constants save_session restore_session` | Review proof coverage and all assumptions; save a session before diagnosis when possible. |

## Tcl, inspection and documentation

report_design_libraries; report_unmatched_points; report_failing_points; report_aborted_points; report_black_boxes; report_dont_verify_points; report_constants. No passing point count alone establishes complete proof.

For Tcl interfaces, construct paths/arguments as Tcl lists, handle collections
using the supported collection APIs, catch errors and inspect explicit command
return values. A syntactically valid Tcl file does not establish command availability.
For native drivers, use their documented input format instead.

```sh
python3 scripts/docs.py search '' --tool formality --limit 20
# Select the installed version/installation when multiple matches exist.
# Retrieve a returned entry with: python3 scripts/docs.py show DOCUMENT_ID
```

The examples run from the bundle directory. Read [command discovery](../../references/command-discovery.md)
for private index creation, bounded retrieval, runtime availability and lifecycle
checks. A manual entry can describe a variable or diagnostic rather than a callable
command. Missing documentation remains a blocker to unsupported command selection.

## Controlled parameters and dependencies

Matching/proof effort only within documented settings; SVF/auto-setup guided by the synthesis methodology. Never set_dont_verify_points or set_black_box to hide a mismatch. Any required abstraction needs explicit functional justification and bounded proof scope.

Shared cell functions, hierarchy, scan/test constants, resets, retiming, DesignWare and synthesis guidance affect matching. synopsys_auto_setup changes interpretation and undriven/test handling: audit its printed assumptions, constants, excluded points and black boxes before accepting a result.

Record original/proposed values, the report-supported hypothesis, manual reference,
valid stage and expected metric. Use [optimization](../synopsys-optimization/SKILL.md)
for bounded comparisons with immutable functionality and hard constraints.

## Failure recovery and verification

Verify the reference/implementation identities, library containers, language, defines, parameters and synthesis guidance. Investigate counterexamples, aborted proofs, excluded points and instantiated black boxes. Failed or inconclusive proof blocks promotion.

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

- [templates/formality.tcl](../../templates/formality.tcl)

Inspect the actual outputs and product-specific reports against the requested
scope. For synthesis/implementation, require mapped/linked artifacts and preserved
constraints; reprove functionality after transformations. For verification,
require complete coverage and clean required checks. For simulation/debug,
require the intended task/test to complete with reviewed diagnostics.

Keep documentation validation, Tcl syntax checks, tool execution, stage acceptance
and end-to-end signoff evidence separate. A generated stream is not a verified
implementation. See [execution contract](../../references/execution-contract.md)
and [validation scope](../../READINESS.md) for the required evidence boundaries.
