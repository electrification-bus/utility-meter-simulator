# Developer guide

## Setup

Python >= 3.11 (developed on 3.14, CI-tested on 3.11 and 3.14), managed with [uv](https://docs.astral.sh/uv/).

```bash
uv sync --group dev
uv run pre-commit install
```

## Gates

These four are what CI runs, in this order. `pre-commit` runs the same set, so a clean commit is a green CI run.

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy --strict src tests
uv run pytest tests
```

The mypy hook in `.pre-commit-config.yaml` runs from the project venv rather than a pre-commit-managed environment. That is deliberate: an isolated environment has no `ebus-sdk`, so it cannot resolve the SDK's real types and silently checks less than CI does. The sibling repo shipped a type error to `main` that way.

## Layout

```
src/ebus_utility_meter_sim/
  __init__.py              # public surface; __version__ lives here (single source of truth)
  exceptions.py            # public exception hierarchy, one root
  py.typed                 # PEP 561 marker: consumers get real types, not Any
tests/
  conftest.py              # paho is patched, so no broker and no socket
  test_package.py          # scaffold-level guarantees
examples/
  utility-meter            # vendored reference publisher; see DESIGN.md
  utility-meter-cfg.example.json
```

The package is a skeleton. The emitter is not built; see [DESIGN.md](DESIGN.md) for what is decided and what is not.

## Testing without a broker

`tests/conftest.py` patches paho's `Client` with a `MagicMock`, so the real SDK and the real `MqttClient` run but no socket opens. The `rec` fixture exposes publishes and subscriptions as `(topic, payload, qos, retain)` tuples, and `rec.retained` computes the effective retained view a late-joining consumer would see, honouring retraction (an empty retained payload deletes the topic rather than recording an empty string).

Assert against `rec.retained` rather than against raw publish order wherever the question is "what would a consumer see", because that is the property that actually matters and it is insensitive to how many times a value was republished.

When a change genuinely needs a broker, run one locally rather than adding a dependency:

```bash
printf 'listener 1883 127.0.0.1\nallow_anonymous true\n' > /tmp/mos.conf
mosquitto -c /tmp/mos.conf
```

## Releasing

Bump `__version__` in `src/ebus_utility_meter_sim/__init__.py`, add the matching `CHANGELOG.md` section, merge, then:

```bash
git tag v0.1.0 && git push origin v0.1.0
```

`publish.yml` re-runs the gates against the tag, refuses to publish if the tag disagrees with `__version__` or if the built wheel is missing required data or contains duplicate entries, publishes via trusted publishing, and creates the GitHub Release from the CHANGELOG section. The publish job is gated on the `pypi` environment, which requires a maintainer's approval.

## Specification tracking

`.ebus-spec.json` pins the specification commit this repo was last reconciled against, plus the capability and device versions it implements. Treat it as a claim that has to stay true: when the emitter lands, add a drift guard in the shape of `ebus-panel-sim`'s `tests/test_catalog_drift.py`, so the pins fail a test rather than quietly going stale.

At scaffold time the pins record what the device model *declares*, not what this package publishes, and the notes field says so.
