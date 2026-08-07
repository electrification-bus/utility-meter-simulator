# Contributing to utility-meter-simulator

Thanks for your interest. This project (`ebus-utility-meter-sim`) is a producer-side [Homie 5](https://homieiot.github.io) publisher and simulator for the [Electrification Bus (eBus)](https://ebus.energy) **utility meter**: the revenue-grade device an electric utility installs at a customer's service entrance. It publishes a spec-conformant `energy.ebus.device.utility-meter` tree so consumers can be built and tested without a revenue meter on the bench.

It is a sibling of [`ebus-panel-sim`](https://github.com/electrification-bus/distribution-enclosure-simulator), which models the distribution enclosure. If you are looking to model a sub-meter or an enclosure's own service-entrance measurements, that is the repo you want; see the table in the README.

**This repository is at scaffold stage.** The packaging, CI and release path are in place; the emitter is not built. [DESIGN.md](DESIGN.md) records the starting point, the specification drift in the vendored reference, the architecture decision already taken (build against `ebus-sdk` directly; do not wait on or copy a shared simulator library), and the decisions still open. Read it before proposing anything substantial.

## How to contribute

- Use [Discussions](https://github.com/electrification-bus/utility-meter-simulator/discussions) for open-ended design questions, and [Issues](https://github.com/electrification-bus/utility-meter-simulator/issues) for defects and concrete proposals.
- For substantive changes (public API surface, the wire model, how utility signals like DOE and price arrive), open a Discussion or Issue first so we can align on scope before you invest the effort.
- **Spec conformance is the north star.** This simulator exists to publish a spec-conformant eBus utility meter. When a PR's behaviour is normative (device state, property contracts, topic structure, capability surface), point to the specification section it implements. If the spec is ambiguous or wrong, file an Issue against the spec repo first and reference it from the PR here.
- **A utility meter is not a metrology device.** Measurements are synthesised. Say so wherever a reader might mistake this for authoritative; it is the one device class where that mistake would matter most.
- **Keep comments to a minimum.** Self-explanatory code, with comments reserved for the non-obvious *why* (a spec quirk, a Homie nuance, a deliberate deviation). Do not add comments that restate the code.
- One commit per logical change is fine; we do not require squash or any particular branch naming.

## What "done" means

This package is published to PyPI, and a PyPI upload can never be replaced. So an increment that lands behaviour and leaves its documentation for later is not a smaller version of the change: it is a release whose docs contradict its code, and the correction costs another release. Ship the whole thing.

A change is done when, in the same PR:

- **Prose it invalidates is fixed.** If a change makes a sentence in the README, `DESIGN.md`, `DEVELOPER.md`, or a docstring untrue, that sentence is part of the change. A new option whose README still describes the old single path is not finished.
- **Types its signatures name are reachable.** A public parameter annotated with a type a caller cannot import from `ebus_utility_meter_sim` forces them to depend on `ebus_sdk` directly, which is what an SDK seam exists to spare them.
- **It carries its `CHANGELOG.md` entry**, under `[Unreleased]` or a version heading.
- **New behaviour has a test that fails without it.** Say so in the PR, and say which. A test that passes against the previous commit is not evidence.
- **Caller obligations are written down where the caller will look.** If correct use requires the caller to do something (wire a callback, set something before connecting, let an event loop turn), a `#` comment in our source does not reach them.

Splitting a change is fine when the parts are genuinely independent, or when a decision is needed that only a maintainer can make. It is not fine as a way to defer the half that needs no decision. If you are unsure which you have, open the PR with the whole thing and let the review split it.

Every example behind that section came from the sibling repo, and from maintainers rather than contributors.

## Local development

Python >= 3.11 (developed and CI-tested on 3.11 and 3.14), managed with [uv](https://docs.astral.sh/uv/). See [DEVELOPER.md](DEVELOPER.md) for the full guide.

```bash
uv sync --group dev                            # create .venv, install runtime + dev deps
uv run pre-commit install                      # install the pre-commit hooks
uv run pytest                                  # tests
uv run ruff check --fix src tests              # lint
uv run ruff format src tests                   # format
uv run mypy --strict src tests                 # type check (strict)
```

Every commit is validated by pre-commit, which runs the same gates CI runs. The mypy hook deliberately runs from the project venv rather than a pre-commit-managed one, so it resolves `ebus-sdk`'s real types instead of silently checking less than CI does.

## Releases

`ebus-utility-meter-sim` is published to [PyPI](https://pypi.org/project/ebus-utility-meter-sim/). Releases are tag-triggered: pushing a `v*` tag runs `.github/workflows/publish.yml`, which re-runs the gates against the tag, builds, asserts the built wheel, uploads via PyPI trusted publishing (OIDC, no stored token), and mirrors the release to GitHub Releases using the tag's `CHANGELOG.md` section.

A release-worthy change bumps `__version__` in `src/ebus_utility_meter_sim/__init__.py`, the single source of truth, and adds a `CHANGELOG.md` entry under a matching `## [x.y.z]` heading. Do not restate the version in `pyproject.toml`; `[tool.hatch.version]` reads it. The publish workflow refuses to upload when the tag and `__version__` disagree, because a PyPI upload can never be replaced.

## Code of conduct

Be decent. Assume good faith, keep criticism about the code, and take disagreements to the evidence: the specification, the wire, or a failing test.
