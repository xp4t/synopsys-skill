# Local configuration

Prepare the Synopsys environment using the user's existing site procedure. Resolve
programs from PATH or supply executable paths in a private manifest. The framework
invokes programs directly, inherits the prepared environment, and does not select
an installation root, license server or startup shell.

Python 3.11 or newer is required. Optional Tcl structural validation uses tclsh;
PDF documentation retrieval uses pdftotext when available. Neither is installed
automatically.

## Private state

Set SNPS_STATE_DIR to a private folder outside the checkout. Otherwise the default
is `$XDG_STATE_HOME/synopsys-skills`, falling back to the user's local state folder.
Generated tool_inventory.json, tool profiles, command_index.sqlite and command
probe evidence belong there. Runtime results can use any private output path;
`runs/` is ignored for local experiments but excluded from public exports.

License configuration is supplied by the user's environment. No license values
are defaulted or distributed. Invocation records redact license settings; raw
vendor logs can still contain private information and must remain private.

## Manifests

Paths to input files, configuration and stage scripts are relative to the manifest
unless absolute. `${BUNDLE_ROOT}`, `${MANIFEST_DIR}` and `${PYTHON}` are resolved
by the loader. Other variables, such as `${TARGET_DB}`, must be explicitly present
in the environment. Missing variables are configuration errors.

Tool executable basenames resolve through PATH; absolute paths preserve their
wrapper name. A tool's optional `environment` object supplies process-local
variables. Script flags in examples are candidates that must be checked against
the installed version before execution.

Declare every transitive design dependency in `inputs`, including sourced Tcl,
logical libraries, includes, netlists, guidance and extracted data. Output/report
paths stay relative to the isolated attempt directory.

The public tool_catalog.json describes tool names and command candidates. It is
not an installed-tool inventory or a guarantee of feature availability.
