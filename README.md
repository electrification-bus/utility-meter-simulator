# ebus-utility-meter-sim

[![CI](https://github.com/electrification-bus/utility-meter-simulator/actions/workflows/ci.yaml/badge.svg)](https://github.com/electrification-bus/utility-meter-simulator/actions/workflows/ci.yaml)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A producer-side [Homie 5](https://homieiot.github.io) publisher and simulator for the eBus **utility meter**: the revenue-grade device an electric utility installs at a customer's service entrance. It publishes a spec-conformant `energy.ebus.device.utility-meter` tree to any MQTT broker, so consumers can be built and tested without a revenue meter on the bench.

> **Status: scaffold.** The packaging, CI, and release path are in place and green. The emitter is not built yet. `examples/utility-meter` carries the pre-existing reference publisher this work starts from; it targets an older revision of the specification and is kept for reference, not as a supported entry point. See [DESIGN.md](https://github.com/electrification-bus/utility-meter-simulator/blob/main/DESIGN.md) for the gap and the plan.

## What a "utility meter" is here

The specification is deliberate that this device is not the same as two things it resembles, and the distinction drives which simulator you want:

| You want to model | Device | Simulator |
| --- | --- | --- |
| The utility's revenue meter at the service entrance | `energy.ebus.device.utility-meter` | **this repo** |
| A distribution enclosure's own service-entrance measurements | `meter` on the enclosure | [`ebus-panel-sim`](https://github.com/electrification-bus/distribution-enclosure-simulator) |
| Branch or per-tenant sub-metering | `meter` on a circuit or lugs device | [`ebus-panel-sim`](https://github.com/electrification-bus/distribution-enclosure-simulator) |

The enclosure's meter and the utility's meter may sit a few feet apart and measure nearly the same current. They are distinct devices, commissioned independently, and may not communicate with each other at all.

## The device it publishes

Per [`devices/utility-meter.md`](https://github.com/electrification-bus/specification/blob/main/devices/utility-meter.md), a utility meter has no eBus-modelled child devices; per-phase measurements are property-name suffixes (`-a`, `-b`, `-c`, `-n`) rather than child devices.

```
ebus/5/<meter-id>/          energy.ebus.device.utility-meter
  info                      Meter identity and nameplate          (always)
  meter                     Instantaneous + cumulative electrical (always)
  status                    Meter-as-device operational state     (always)
  grid                      Verdict view of utility supply health (when signalled)
  doe                       Utility-signalled import/export limits (when signalled)
  price                     Import/export price schedules          (when signalled)
  demand                    Peak-average demand quantities         (when computed)
  power-quality             Quantitative power-quality measurements (when computed)
```

## Requirements

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/)
- An MQTT broker. The companion [broker-quickstart](https://github.com/electrification-bus/broker-quickstart) bundle brings one up in one command; any `mosquitto` works.

## Install

```bash
pip install ebus-utility-meter-sim    # or: uv add ebus-utility-meter-sim
```

The import package is `ebus_utility_meter_sim`. For local development, pin a path instead:

```toml
ebus-utility-meter-sim = { path = "../utility-meter-simulator", editable = true }
```

## Development

```bash
uv sync --group dev
uv run pre-commit install
uv run pytest
uv run ruff check --fix src tests
uv run ruff format src tests
uv run mypy --strict src tests
```

See [DEVELOPER.md](https://github.com/electrification-bus/utility-meter-simulator/blob/main/DEVELOPER.md) for the full guide and [CONTRIBUTING.md](https://github.com/electrification-bus/utility-meter-simulator/blob/main/CONTRIBUTING.md) before opening a PR.

## Licence

MIT. See [LICENSE](https://github.com/electrification-bus/utility-meter-simulator/blob/main/LICENSE).
