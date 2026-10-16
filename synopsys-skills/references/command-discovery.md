# Version-aware command retrieval

Build a private index from the actual installation. The index records original
manual paths, tool/version/installation, descriptions and hashes; it does not
redistribute manuals. Diagnostic messages, variables and utility documents are
not all callable commands.

```sh
python3 synopsys-skills/scripts/discover.py --root "$SNPS_INSTALL_ROOT" --output "$SNPS_STATE_DIR/tool_inventory.json"
python3 synopsys-skills/scripts/docs.py build --inventory "$SNPS_STATE_DIR/tool_inventory.json"
python3 synopsys-skills/scripts/docs.py search write_gds --tool ic-compiler-ii --limit 5
# Retrieve an id returned by search:
python3 synopsys-skills/scripts/docs.py show DOCUMENT_ID --lines 100
```

Select --version and --installation when multiple releases are present. Search
ranks exact names first. Retrieval verifies the original file hash and returns
bounded numbered text; read further ranges for syntax, arguments, defaults,
restrictions, license requirements, stage prerequisites and examples. A changed
manual requires a new index. Keep prior indices for historical run evidence.

In Tcl shells that support them, inspect `info commands`, namespace-specific
commands, `help -groups`, `help -verbose COMMAND` and `man COMMAND`. Verify the
product's interface first: compiler, debug, circuit and verification drivers have
different help mechanisms and input formats. Use templates/commands.tcl only
where its commands are supported. Record any runtime registry with its actual
executable/version provenance in private state.

Mark selected operations as observation, derived-state update, design mutation,
session/environment mutation or export after reading their side effects. Names
such as report/check/get are lookup hints, not a guarantee of no state changes.
Presence in a registry does not establish correct stage, mode, license or arguments.

Lifecycle wording in a manual is a hint: determine whether it refers to a whole
command or only an option. Verify any replacement against the installed release.
Absent or incomplete documentation is a real limitation; do not invent commands,
extraction controls or physical verification rules.

index_supplements.py can add locally available driver help, Library Manager
manuals, plaintext verification declarations and utility HTML from the chosen
inventory. Encrypted definitions are not decoded. Store this generated index and
all captured vendor output outside the public repository.
