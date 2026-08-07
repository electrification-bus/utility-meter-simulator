# ebus-utility-meter-sim design

This document records the starting position, the gap between it and the current specification, and the decisions still open. It is written at scaffold time and should be revised as the emitter is built, not left to rot.

## The starting point

`examples/utility-meter` is a working single-file reference publisher, vendored verbatim from `python-sdk/examples/utility-meter` at the time this repo was created. It is 862 lines and publishes a complete utility-meter device, including a small HTTP endpoint that stands in for the utility's out-of-band backhaul for DOE envelopes and price schedules.

It is kept because it is the only working implementation of this device model and encodes real decisions worth preserving: the DOE and price properties as `json` values carrying a `$format` JSONSchema, validation of posted bodies before publish, and the HTTP shape for injecting utility signals at runtime.

It is **not** the supported entry point, and is not imported by the package. It targets an older revision of the specification (see below), and its architecture is a single script rather than a library a producer can drive.

## Specification drift in the vendored reference

Measured at scaffold time against specification commit `4254526`:

| | Reference targets | Specification now |
| --- | --- | --- |
| Data model version | 0.3 | **0.6** |
| Document path | `data-models/utility-meter.md` | **`devices/utility-meter.md`** |

Three minor revisions and a file move. The reference's module docstring cites a path that no longer resolves. Nothing here says the reference is wrong on the wire; it says nobody has checked it since 0.3, and the assumption should be that it is wrong somewhere until a drift audit says otherwise.

That audit is the first substantive task, and it should be mechanical rather than impressionistic: pin the capability versions (below), then diff what the reference publishes against what the current capability catalogs declare, property by property.

## Capability surface

Per `devices/utility-meter.md` 0.6, the device carries three capabilities always and five when the corresponding signal exists:

- **Always**: `info`, `meter`, `status`. These define what the device is.
- **When signalled or computed**: `grid`, `doe`, `price`, `demand`, `power-quality`.

There are no eBus-modelled child devices. Per-phase measurements are property-name suffixes (`-a`, `-b`, `-c`, `-n`); system aggregates carry no suffix. This is materially simpler than the distribution-enclosure tree `ebus-panel-sim` publishes, which is a parent with a device per circuit, lugs pair and DER.

### A specification inconsistency to resolve

`devices/utility-meter.md` 0.6 contains a contradiction worth filing upstream before building against it. The ASCII device tree in *Utility Meter Device* lists seven capabilities and omits `price`; the prose immediately below it reads "The latter five (`grid`, `doe`, `price`, `demand`, `power-quality`)", which counts `price` in. The prose and the registry agree with each other, so the tree is the likely error, but this repo should not silently pick one.

## Open decisions

**How much of `ebus-panel-sim`'s architecture applies.** That package separates identity (a manifest, read once at startup) from telemetry (derived per tick from a small driving signal), and resolves the wire surface through vendored spec catalogs, profile JSON and mapping YAML. The split earns its keep there because the tree is large and the device types are many.

A utility meter is one device with no children. The manifest/mapping/profile machinery may be more than this needs, or it may be exactly what keeps the two simulators consistent and lets the catalog-drift guard work the same way. Decide deliberately rather than by defaulting to either answer, and record the reasoning here.

**Where the utility's signals come in.** The reference exposes an HTTP endpoint for DOE and price. Whether that belongs in the library, in an example, or in a separate driver is unsettled. It is the one part of this device that is genuinely inbound, and it should not be designed by accident.

**What "simulation" means for a revenue meter.** The reference synthesises measurements from a config file and says so plainly: it is a publisher reference, not a metrology device. That is the right posture, and the docs should keep saying it, because a revenue meter is exactly the device someone might mistake for authoritative.

## What this repo inherits deliberately

The packaging, CI, release and review conventions are copied from `ebus-panel-sim` rather than reinvented, including several that exist because something went wrong there:

- The wheel is asserted in `publish.yml`, because that package shipped four releases before anyone noticed its wheel had never built. The test suite reads the source tree and cannot catch it.
- `py.typed` ships from the first release, because shipping a `mypy --strict` package without the marker means consumers resolve it to `Any`.
- The version is single-sourced from `__version__`, and the publish workflow refuses a tag that disagrees with it.
- `CONTRIBUTING.md` carries a definition of done, because on a published package a deferred documentation fix is a second release.
