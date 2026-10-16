---
name: synopsys
description: Use when selecting Synopsys EDA tools or starting an ASIC RTL-to-GDSII task in a user-configured environment.
---

# Synopsys engineering entry point

Resolve the canonical skill directory to locate shared scripts and references.
Use [RTL-to-GDSII orchestration](../synopsys-rtl2gds/SKILL.md) for requests such
as “generate verified GDSII from this RTL,” including autonomous diagnosis and
controlled timing/area optimization. Load only the tool skills needed next.

Read [environment](../synopsys-environment/SKILL.md) and the user-provided local inventory before invoking a tool. Discover actual versions, wrapper paths, documentation and prerequisites.

| Work | Skill |
| --- | --- |
| RTL analysis/synthesis | [Design Compiler](../synopsys-design-compiler/SKILL.md) |
| Formal equivalence | [Formality](../synopsys-formality/SKILL.md) |
| NDM references | [Library Manager](../synopsys-ndm-library-manager/SKILL.md) |
| Digital physical implementation | [ICC2](../synopsys-ic-compiler-ii/SKILL.md), [Fusion](../synopsys-fusion-compiler/SKILL.md) |
| Extracted timing | [PrimeTime](../synopsys-primetime/SKILL.md) |
| Extraction/physical verification | [StarRC](../synopsys-starrc/SKILL.md), [ICV](../synopsys-ic-validator/SKILL.md) |
| Simulation/debug/stimulus | [VCS](../synopsys-vcs/SKILL.md), [Verdi](../synopsys-verdi/SKILL.md), [VCPS](../synopsys-vc-portable-stimulus/SKILL.md) |
| Circuit/custom design | [HSPICE](../synopsys-hspice/SKILL.md), [Custom Compiler](../synopsys-custom-compiler/SKILL.md) |
| Legacy/embedded/GUI | [ICC](../synopsys-ic-compiler/SKILL.md), [VC Static](../synopsys-vc-static/SKILL.md), [Design Vision](../synopsys-design-vision/SKILL.md) |
| Failures/PPA | [Troubleshooting](../synopsys-troubleshooting/SKILL.md), [Optimization](../synopsys-optimization/SKILL.md) |

Use [command discovery](../../references/command-discovery.md) to retrieve local
syntax/defaults/restrictions/examples on demand. Read the original manual and
verify availability/state prerequisites. Index matches include diagnostics and
variables; they are not all executable commands.

Working shells do not establish technology, feature licenses or physical readiness. Report local blockers with private evidence rather than assuming a complete installation.

Run reviewed scripts through [execution contract](../../references/execution-contract.md).
Keep original RTL and hard constraints fixed, preserve every attempt, gate
transformations on equivalence and distinguish stream generation from qualified
final-stream signoff. Do not install software, alter global configuration or
commit work without the user's authorization.
