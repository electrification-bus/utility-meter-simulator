"""ebus-utility-meter-sim — producer-side Homie publisher for the eBus utility meter.

Publishes an eBus **utility meter** (`energy.ebus.device.utility-meter`, per
`devices/utility-meter.md` in the Electrification Bus specification) as a
Homie 5 device tree over MQTT, so consumers can be built and tested without a
revenue meter on the bench.

A utility meter in eBus is specifically the revenue-grade device the utility
installs at the service entrance. The specification is deliberate that this is
NOT the same thing as:

- a **sub-meter**, which is a ``meter`` capability on whatever device it attaches
  to (a circuit, a feedthrough lugs device), and
- a **panel meter**, which is the ``meter`` a distribution enclosure publishes for
  its own service-entrance measurements, at the enclosure's main relay rather
  than at the utility's revenue boundary.

Those two are modelled by ``ebus-panel-sim``. This package models the third.

Status: scaffold. The package skeleton, packaging, CI and release path are in
place; the emitter is not built yet. ``examples/utility-meter`` carries the
pre-existing reference publisher this work starts from. See DESIGN.md for the
gap between that script and the current specification.
"""

from __future__ import annotations

from ebus_utility_meter_sim.exceptions import (
    ConfigValidationError,
    EmitterStateError,
    UtilityMeterSimError,
)

# Single source of truth for the distribution version: pyproject reads it from here
# via `[tool.hatch.version]`, and publish.yml refuses to release when the git tag
# disagrees. Bump it in this one place.
__version__ = "0.1.0"

__all__ = [
    "ConfigValidationError",
    "EmitterStateError",
    "UtilityMeterSimError",
    "__version__",
]
