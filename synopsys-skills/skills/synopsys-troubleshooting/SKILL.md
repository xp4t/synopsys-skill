---
name: synopsys-troubleshooting
description: Use when a Synopsys command or implementation stage fails, produces suspicious reports, crashes, stalls, or reports license, timing, connectivity, or physical violations.
---

# Evidence-driven recovery

Read the owning tool skill and [execution contract](../../references/execution-contract.md).
Start with `console.log`, `execution.json`, `decision.json`, tool internal logs,
required reports, incoming checkpoint hashes and input/script/config versions.
An exit code of zero is insufficient: inspect internal diagnostics, required outputs and verification results.
Source-script echoes containing error strings are not necessarily actual errors;
read anchored severity messages and the executed command context.

```sh
python3 scripts/flow.py diagnose /absolute/console.log
```

Classification is triage, not a root-cause verdict or signoff parser. Retrieve the
exact diagnostic/command manual from the index. For every attempted correction,
record evidence, category, causal hypothesis, old/new values or corrected command,
documentation, restore point, affected downstream stages and measured outcome.

| Category | Investigate and correct | Restart/promotion rule |
| --- | --- | --- |
| Invalid command/options | Wrapper/product/version, man syntax, command registry, Tcl list quoting and current mode | Correct reviewed script; unchanged specs; fresh attempt |
| Missing input/library/technology | Paths, RTL file order, defines/top, .db/NDM/RC/maps/decks, cell names/schema/units | Restore valid dependencies; invalidate all stale consumers |
| RTL elaboration/latches/drivers | Elaboration hierarchy, parameterization and functional intent | No deleting modules or behavioral RTL edits without authorization |
| Constraints/unconstrained paths | Clocks/generated clocks/IO delays/exceptions, path classes and coverage | Correct from requirements; never remove constraints to hide failure |
| Negative timing | Setup versus hold, exact corner/path, logic/net delay, slew/load and clock effects | Target documented synthesis/physical ECO; reverify logic and all affected signoff |
| Density/congestion | Local hot spots, macro channels, pin access, PG consumption and routing layers | Authorized utilization/placement/routing changes; restore before earliest affected stage |
| CTS/connectivity | Clock definitions/sinks/gating, allowed cells/rules, PG/clock opens and scenario setup | Repair missing configuration before skew/effort tuning |
| Routing/DRC/antenna | Unrouted nets, geometry rules, pin access, missing views/maps, real deck IDs | Target repair; regenerate extraction and final physical checks |
| LVS/formal mismatch | Opens/shorts/device/net mapping, reference identity, SVF/test constants, black boxes and counterexamples | No promotion until mismatch/proof coverage is resolved |
| License | Exact endpoint, feature and checkout status; time-limited transient retry | Same design/config; stop on missing feature or budget exhaustion |
| Loader/unsupported configuration | Canonical wrapper/env, platform ABI, actual missing libraries, technology/schema support | Process-local justified correction; no arbitrary .so borrowing or software install |
| Crash/OOM/timeout | Tool trace, last command, process/resource evidence, data volume, supported thread/memory controls | Fresh process from valid checkpoint; reduce resource demand without dropping required scope |

Use the actual product/version documentation for wrapper dispatch, missing runtime libraries, unsupported commands, library linking, license features and native help interfaces. Do not promote an environment failure into a design-tuning experiment.

For tuning, use only authorized bounded parameters and one causal experiment at
a time. Compare all required metrics and verification results, retain the baseline
on regression, and stop after configured attempts/time/no-improvement. Preserve
logs and immutable checkpoints even for rejected candidates. If no justified
correction remains, report a genuine blocker with the missing input or environment
repair; do not blindly repeat or manufacture success.
