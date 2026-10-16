# Synopsys EDA skills

Portable engineering skills for Claude Code and Codex: RTL preparation, synthesis,
formal equivalence, physical implementation, extraction, timing, verification and
controlled PPA experiments.

The repository contains reusable instructions and scripts. Each user supplies
installed tools, licenses, documentation and qualified technology inputs. Generated
inventories, documentation indices, run logs and design results stay in private
local storage and are not distributed with the skills.

## Quick start

Python 3.11 or newer is required for the framework. Prepare your tools using your
organization's normal environment setup; the skills do not prescribe a startup
shell or installation path.

From the repository root, expose the skills in a project:

```sh
python3 synopsys-skills/scripts/install.py --project .
```

Codex discovers `.agents/skills`; Claude Code discovers `.claude/skills`. Both use
project-local links to the canonical skills. Use `$synopsys-rtl2gds` in Codex or
`/synopsys-rtl2gds` in Claude Code, or request an RTL-to-GDSII flow in natural language.
See [platform integration](references/platform-integration.md) for other projects.

## Configure a design

Resolve tool executables from PATH or a private tool profile. Supply the actual
RTL/top, functionality, constraints, technology/reference libraries, extraction
models, stream maps and required signoff decks. No example specifies a user's
process, installation, license server or timing target.

[The counter example](examples/USAGE.md) has its own explicit teaching specification.
It requires a user-selected logical library and does not supply a physical PDK.
Manifest paths may be relative to the manifest, or use `${BUNDLE_ROOT}` and explicit
environment variables such as `${TARGET_DB}`. Missing variables fail configuration.

```sh
python3 synopsys-skills/scripts/flow.py preflight synopsys-skills/examples/counter/chain.manifest.json --partial
python3 synopsys-skills/scripts/flow.py run synopsys-skills/examples/counter/chain.manifest.json --partial --out runs/counter-001
```

The executor invokes the configured program directly using the already prepared
environment. It retains every attempt and validates status, reports, checks and
artifacts before promotion. Read [the execution contract](references/execution-contract.md).

## Installation discovery and documentation

Inventories and indices are generated locally, not shipped. Set SNPS_INSTALL_ROOT
to your chosen installation location and SNPS_STATE_DIR to a private writable state
folder outside the repository. The default state location follows XDG conventions.

```sh
python3 synopsys-skills/scripts/discover.py --root "$SNPS_INSTALL_ROOT" --output "$SNPS_STATE_DIR/tool_inventory.json"
python3 synopsys-skills/scripts/docs.py build --inventory "$SNPS_STATE_DIR/tool_inventory.json"
python3 synopsys-skills/scripts/docs.py search write_gds --tool ic-compiler-ii
```

See [command discovery](references/command-discovery.md) for bounded retrieval,
release/installation selection and runtime command validation. Vendor manuals,
proprietary models and foundry decks must remain in the user's licensed environment.

## Validation and publication

```sh
python3 -m unittest discover -s synopsys-skills/tests -v
python3 synopsys-skills/scripts/validate.py
python3 synopsys-skills/scripts/export_public.py --out dist/public-source
```

The exporter selects reviewed source categories and rejects common private-data
patterns. Generated logs, databases, tool profiles, license information and design
results are excluded. Keep credentials and confidential inputs outside the source
tree; review the exported tree before publishing. Existing Git history, if any,
requires a separate check because exporting current files does not rewrite history.

[Validation scope](READINESS.md) distinguishes framework tests from executed ASIC
stages. A generated GDSII file is not a verified signoff-clean implementation.

## Layout

- `skills/`: independently discoverable product and workflow skills.
- `scripts/`: discovery, documentation retrieval, execution, recovery, optimization
  and validation.
- `templates/`: Tcl building blocks with explicit design/technology configuration.
- `examples/`: portable teaching RTL and configurable manifests.
- `references/`: public operating contracts and a generic tool catalog.

The orchestration entry point is [synopsys-rtl2gds](skills/synopsys-rtl2gds/SKILL.md).
