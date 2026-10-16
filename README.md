# Synopsys EDA Skills

Help Claude Code and OpenAI Codex work with Synopsys tools for ASIC design, from RTL preparation to GDSII generation.

## What it includes

- Tool skills for Design Compiler, IC Compiler II, Fusion Compiler, PrimeTime, Formality, VCS, and more.
- RTL-to-GDSII workflow instructions and reusable Tcl templates.
- Failure diagnosis, checkpoint recovery, and controlled power, performance, and area optimization.
- Scripts for finding installed tools, searching local documentation, and tracking runs.

## What you need

- Claude Code or OpenAI Codex.
- Python 3.11 or newer.
- Installed Synopsys tools with valid licenses and your normal environment setup.
- Your RTL, design constraints, and the libraries and technology files needed for your flow.

Tools, licenses, and technology files are supplied by you. No particular installation path or startup shell is required.

## Get started

Clone this repository and open it in your terminal. From the repository root, run:

```sh
python3 synopsys-skills/scripts/install.py --project .
```

This makes the skills available through `.claude/skills` for Claude Code and `.agents/skills` for Codex. Start your agent in this project, then ask:

> Use the Synopsys skills to inspect my RTL and available tools, identify missing inputs, and plan an RTL-to-GDSII flow. Preserve functionality and timing requirements, recover from supported failures, and report any blockers.

You can also select `/synopsys-rtl2gds` in Claude Code or `$synopsys-rtl2gds` in Codex.

## Learn more

- [Detailed setup and configuration](synopsys-skills/README.md)
- [Example design and usage](synopsys-skills/examples/USAGE.md)
- [Using the skills in another project](synopsys-skills/references/platform-integration.md)
- [Validation scope and limitations](synopsys-skills/READINESS.md)

Keep private configuration, licenses, foundry files, and run results outside the public source. A generated GDSII file counts as signoff-clean only when the required verification checks pass.
