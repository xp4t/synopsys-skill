# Claude Code and Codex integration

Canonical skills live in `synopsys-skills/skills/synopsys-name`. The installer
creates project-local links in `.agents/skills` for Codex and `.claude/skills` for
Claude Code. Existing conflicting entries are never overwritten.

From the repository root:

```sh
python3 synopsys-skills/scripts/install.py --project .
python3 synopsys-skills/scripts/install.py --project . --check
```

Use another project path with --project to expose the same collection there.
Keep the bundle accessible; if moved, reinstall/check the links. Resolve a linked
skill's canonical location before accessing shared resources two parents above it.

Codex uses `$synopsys-rtl2gds`; Claude Code uses `/synopsys-rtl2gds`. Descriptions
also support natural-language activation. Confirm discovery in the installed
client after installation; metadata checks do not prove successful agent execution.

Platform conventions are described in the official
[Codex skills guide](https://developers.openai.com/codex/skills/) and
[Claude Code skills guide](https://code.claude.com/docs/en/skills).

Client authentication and tool/license configuration are local responsibilities.
No personal configuration, client logs or credentials are included in this bundle.
