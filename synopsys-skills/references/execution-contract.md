# Execution, result and recovery contract

## Scope and trust

Python 3.11 or newer is required. Runtime helpers use only its standard library.
Stage Tcl/Python and the configured environment are trusted,
reviewed engineering code, not sandboxed programs. The framework enforces evidence
and bookkeeping gates; it cannot prove an agent's report adapter interprets every
PDK rule correctly. Review adapters against the installed manuals and real reports.

Every new run/attempt/checkpoint has a fresh directory. Existing run directories
are refused. No shell command strings are constructed from design paths; the configured program
receives preserved argv and its wrapper filename from the prepared environment. stdin is closed;
all scripts must terminate. Timeout kills the owned process group, including
helpers that survive their dispatcher. Remote/distributed jobs require their
tool's documented job cancellation and scheduler evidence as well; a local
process group cannot cancel remote compute jobs.

## Manifest

Use JSON with input/configuration paths relative to the manifest or explicitly absolute.
Environment variables and executable lookup follow configuration.md. Runtime
artifacts/reports are relative to the current attempt directory and cannot escape.
The example manifests under examples/counter are complete stage experiments.
examples/full-flow-contract.json records a full technology/stage contract and
intentionally fails preflight until populated with actual qualified inputs.

Required fields: design identifier, top, RTL list, SDC, requirements, tools, stages.
Optional config_tcl is sourced by templates. **Declare every additional/transitive
input in inputs**: target .db libraries, include files, sourced Tcl, implementation
netlist/SVF, UPF, parasitics, generated constraint sources and methodology recipes.
The runner cannot infer dynamic Tcl dependencies; undeclared dependencies are a
configuration error. Full preflight additionally requires the complete technology
contract and ordered stage chain.

Tool entries contain executable, startup_args and script_option; resolve their
values from the user's environment and verify the installed interface. For native drivers,
use execution.execute directly with their documented argv or a reviewed adapter;
do not force VCS/StarXtract/ICV/SPICE inputs into the Tcl manifest interface.

Each stage declares id, tool, script, timeout_s, artifacts, checkpoint_artifacts,
metric_limits and any extra required_checks. Artifact paths must name actual
newly written outputs. Checkpoint complete databases and dependent metadata,
including NDM libraries or a Formality session; a label alone cannot restore state.
Use unique basenames within a checkpoint. Restores are new writable copies under
restores/stage-attempt; accepted checkpoints remain unchanged.

Recovery/optimization parameters are declared in parameters and allowed_parameters:

```json
{
  "parameters": {"core_utilization": 0.65, "synthesis_map_effort": "medium"},
  "allowed_parameters": {
    "core_utilization": {"min": 0.45, "max": 0.70},
    "synthesis_map_effort": {"choices": ["medium", "high"]}
  },
  "max_attempts": 3,
  "license_retries": 1,
  "license_backoff_s": 10,
  "wall_budget_s": 14400
}
```

The launcher passes SNPS_STAGE, SNPS_ATTEMPT, SNPS_TOP, SNPS_FRAMEWORK_ROOT,
SNPS_CONFIG_TCL, SNPS_PARAMETERS_JSON, SNPS_PARAM_name and checkpoint/restore paths.
The stage's Tcl adapter uses `snps_parameter name default_value`. It must actually
apply the recorded value and report it. Do not modify requirements, RTL, SDC,
corners, operating conditions or verification scope during a candidate search.

## Results and promotion

Retain console.log, internal tool logs, invocation.json, execution.json,
decision.json, report files, generated outputs and checkpoint manifests. The
runner snapshots reviewed stage scripts and hashes protected inputs, the shared
Tcl helper, scripts and checkpoints. Declared paths and resolved identities are
retained separately, so symlink retargeting also invalidates results. Before/after hashes detect stale/mutated
inputs. effective-manifest.json records accepted recovery scripts/parameters;
summary.json records all attempts and accepted/rejected decisions.

Scripts emit result.json only after meaningful tool queries/report evaluation:

```json
{
  "schema_version": 1,
  "status": "pass",
  "checks": {"equivalence": true, "proof_coverage_clean": true},
  "metrics": {},
  "reports": ["reports/equivalence.rpt", "reports/failing.rpt"]
}
```

Every required check must be JSON Boolean true; strings/absence fail. Reports
must exist and be nonempty. Every declared artifact must exist. Metrics in limits
must be finite and satisfy bounds. The mandatory check list is in policy.CHECKS;
review it when adding adapters. Checks must derive from actual evidence, never
unconditional success constants for unexecuted physical stages. In physical
stages, include functional equivalence after logical ECOs, or demonstrate unchanged
logical netlist identity with preserved prior proof. The orchestrator must add
the associated required check/report before executing a transforming adapter.

The shipped DC/formal examples emit supported checks from actual tool returns.
The strict Formality adapter also requires recognized no-failing/unmatched/aborted,
no-excluded/user-constant reports and no instantiated black boxes. Unused macro
entries with Instances: 0 are retained as evidence; intentional proof abstractions
need a separately reviewed, explicitly scoped methodology adapter.
Other PDK-dependent templates intentionally do not emit result.json: the qualified
flow/report adapter must supply it after checking their actual reports and state.
Missing result is a rejection, not a deferred automatic pass. Templates are
operational building blocks, not a fabricated universal foundry flow.

Full mode requires all ordered stages, required technology inputs, explicit nonempty
corners/modes, a finite positive clock period, setup/hold WNS lower bounds of at
least zero, timing hard limits and final-stream DRC/LVS/antenna checks. Placement,
CTS and routing also require functional_equivalence evidence automatically in full
mode; an adapter may establish unchanged logical netlist identity plus prior proof.
`requirements.ir_em_required` must
be explicitly Boolean; true adds IR and EM gates. EM/IR capability and qualified methodology must be validated locally. A structurally framed GDS record stream alone
proves neither valid geometry nor physical signoff. GDS integrity additionally
checks HEADER/BGNLIB/ENDLIB framing and hashes the output.

`partial-stage-validated` means only the selected stages passed the trusted
adapters and retained evidence. Full `end-to-end-validated` means the configured
chain passed; final reports must still state technology/deck/coverage scope and
actual objectives. Never present a partial stage result as verified GDSII.

## Diagnosis, recovery and bounded optimization

Automatic classification is triage. Read relevant logs/reports/design state and
exact local manuals before adding recovery_candidates to a stage. Each candidate
contains category, reason, documentation, changes with parameter/old/new and a
reviewed script. A command/input/environment correction can use an empty changes
list; parameter tuning is rejected for license, library, RTL, constraints, formal,
unsupported technology, crash/OOM/timeout and invalid-command categories.

The runner tries only matching, documented candidates within max_attempts and the
shared run deadline. License retries use the same script/config and separate
budget; backoff is bounded by remaining time. Exhausted budget/no candidate means
blocked, with an actionable diagnosis. Changing inputs requires a new run and
invalidates all downstream results. Keep/revert decisions never erase history.

optimize.py runs a feasible verified baseline and configured candidate list.
It replays the selected chain, including formal/signoff in full mode, rather than
reuse stale downstream evidence. It keeps the accepted effective configuration.
Set explicit min/max direction for **every regression guardrail** (TNS, WNS and
slack normally maximize; power/area normally minimize). Missing directions or
metrics reject candidates. Define hard bounds, absolute/relative improvement
thresholds, max_trials, wall_budget_s and max_no_improvement. All trials remain
available, while the best_run pointer identifies the accepted result. A blocked
baseline requires failure recovery before feasible-PPA optimization.

Snapshots, hashing/copy bookkeeping and process termination can add overhead to
an execution deadline; tool execution and retry backoff are capped by remaining
budget. Do not use this local runner as a hard real-time scheduler.
