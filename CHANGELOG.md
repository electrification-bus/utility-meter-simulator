# Changelog

## [Unreleased]

### Added

- Repository scaffold: packaging (hatchling, single-sourced `__version__`, `py.typed`, PEP 639 licence metadata), CI on Python 3.11 and 3.14, tag-triggered PyPI publishing via trusted publishing, pre-commit running the same gates CI runs, and the shared paho-patching test harness. Conventions are copied from `ebus-panel-sim` rather than reinvented; several exist because something went wrong there, and `DESIGN.md` records which.
- `examples/utility-meter`: the pre-existing single-file reference publisher, vendored verbatim from the `ebus-sdk` examples tree as the starting point. It targets specification data model 0.3 while the current document is 0.6 and has moved to `devices/utility-meter.md`, so it is kept for reference rather than as a supported entry point. The drift audit is the first substantive task.
