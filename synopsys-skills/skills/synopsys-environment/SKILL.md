---
name: synopsys-environment
description: Use when discovering Synopsys tools, locating their local documentation, validating configuration, or diagnosing startup and license availability.
---

# Local tool environment

Use the user's prepared environment and configured executables. Do not assume an
installation root, operating account, license endpoint, product version or startup
shell. Resolve each tool independently; similar products can have different driver
options and supported modes.

Read [configuration](../../references/configuration.md) before the first run.
Discover the selected installation into private local state:

```sh
python3 scripts/discover.py --root "$SNPS_INSTALL_ROOT" --output "$SNPS_STATE_DIR/tool_inventory.json"
```

The command runs from the bundle directory. SNPS_INSTALL_ROOT is user-provided;
SNPS_STATE_DIR is a private writable folder. Discovery examines installation files
without executing binaries or changing configuration. Validate the selected wrapper,
actual version/build, documentation, script interface and feature availability
before design execution. A directory label alone is not an executed build result.

Use PATH or explicit private tool profiles to select executables. Preserve product
wrapper names. Invoke the configured program directly from the prepared environment;
no shell launcher is required by these skills. Any environment repair should be
process-local, justified by diagnostics and within the user's authorized scope.
Never edit existing site/user configuration or install missing software implicitly.

Inspect license errors for the requested feature using the user's configuration.
Do not invent server settings or substitute endpoints. License-utility availability
must itself be discovered. A successful shell session proves only features actually
used at that time. Bound transient checkout retries; unavailable features or broken
configuration are genuine blockers.

Require complete diagnostics and expected completion for startup probes. A version
banner or process status zero can coexist with internal loader/library errors.
Keep all inventories, identifiers, logs and license diagnostics private. Use
[troubleshooting](../synopsys-troubleshooting/SKILL.md) for evidence-based recovery.
