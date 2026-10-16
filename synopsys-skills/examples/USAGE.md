# Configurable counter example

The example RTL is an 8-bit incrementing counter with active-low asynchronous reset.
Its testbench checks reset and 20 cycles. The SDC explicitly defines a 10 ns teaching
specification; it is not a default timing requirement for other designs.

Supply a suitable logical library through TARGET_DB and make the selected tools
available in the prepared environment. No technology library is distributed.
From the repository root:

```sh
python3 synopsys-skills/scripts/flow.py preflight synopsys-skills/examples/counter/chain.manifest.json --partial
python3 synopsys-skills/scripts/flow.py run synopsys-skills/examples/counter/chain.manifest.json --partial --out runs/counter-chain-001
python3 synopsys-skills/scripts/optimize.py synopsys-skills/examples/counter/chain.manifest.json synopsys-skills/examples/counter/optimization-plan.json --partial --out runs/counter-optimization-001
```

The chain runs synthesis followed by Formality using the newly produced checkpoint.
The optimization plan compares supported medium/high mapping effort, preserves the
clock specification, checks reported timing feasibility/regression, rechecks proof
coverage and keeps only sufficient verified improvement. Inspect actual report units
before interpreting metrics. Results depend on the user's library and installation.

The controlled recovery manifest deliberately invokes an invalid command, then
uses a documented RTL analysis/check script as its matching correction. It changes
neither RTL nor constraints. Use a new output directory for each run.

The standalone formal manifest requires IMPLEMENTATION_NETLIST and SYNTHESIS_SVF.
The chain manifest supplies its handoff through a fresh restore directory instead.
Native simulation and ideal-RC examples require their own configured drivers and
explicit completion/measurement checks; no simulator installation is assumed.

For physical execution, populate the full technology contract and replace all
missing PDK/report adapters. A logical-only result is partial evidence and cannot
be called a verified GDSII implementation. Keep all generated reports and design
artifacts private.
