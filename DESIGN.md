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

## Decided: how much of `ebus-panel-sim`'s architecture applies

**Copy nothing yet, and do not wait on a shared library.** Build this simulator against `ebus-sdk` directly. Revisit sharing once there is a real emitter here to compare against, which is the first moment two implementations exist rather than one plus a guess.

The reasoning, from an analysis of `ebus-panel-sim` run on 2026-08-07 (six independent investigations, each recommendation attacked by two further reviewers on correctness and on cost):

**The wire layer is genuinely device-agnostic, and that is not the constraint.** Its seven modules plus `exceptions.py` and `manifest.py` form a closed subgraph with exactly one panel-domain import, reachable only through `bag_builder.py`. This was proved rather than argued: the closure was copied out, an import hook was installed that raises on any `ebus_panel_sim` import, and a three-phase utility meter was driven through it successfully. A full migration in a scratch checkout came to `164 passed`, `mypy --strict` clean, with zero test-file edits and zero `emitter.py` edits.

That cheapness is the argument for waiting rather than for acting. Moving this code later costs about what it costs now, so there is nothing to buy by moving early, and something real to lose: an API derived from one implementation and validated against that same implementation.

**The highest-value pieces are not simulator-common at all; they belong upstream.** The teardown and transport-ownership correctness (`_sdk_seam.py`) is an `ebus-sdk` gap, filed as [python-sdk#46](https://github.com/electrification-bus/python-sdk/issues/46): `Device` models three teardowns and implements one. The paho test harness in `tests/conftest.py` patches another package's internals, which makes the SDK its honest home. Diff-only publishing is a producer concern the SDK is already partway to owning. For these, the rule of three does not apply, because what that rule prices is the cost of *creating* a shared home, and the home already exists. Waiting for a third simulator to reimplement `$state=lost` incorrectly is not a policy.

**What this repo should therefore do**: depend on `ebus-sdk`, adopt whatever it grows, and write the meter's own wire handling in whatever shape the meter actually needs. If that shape converges on panel-sim's, the later extraction is cheap and will then be justified by two real consumers. If it diverges, nothing was prematurely frozen.

One candidate is worth watching specifically. `profile_loader.py`'s `_expand_pattern` already implements per-phase suffix expansion (`-a`/`-b`/`-c`/`-n`) driven by the spec's own capability catalogs, which is precisely this device's defining shape, and the SDK has no equivalent. In the experiment above, a meter profile that selected `voltage-a` by name alone had `datatype=float, unit=V` hydrated straight from the catalog. If catalog-driven hydration is wanted here, that is the piece to reach for first, and it may justify a shared home before a third consumer exists.

## Still open

**Where the utility's signals come in.** The reference exposes an HTTP endpoint for DOE and price. Whether that belongs in the library, in an example, or in a separate driver is unsettled. It is the one part of this device that is genuinely inbound, and it should not be designed by accident.

**What "simulation" means for a revenue meter.** The reference synthesises measurements from a config file and says so plainly: it is a publisher reference, not a metrology device. That is the right posture, and the docs should keep saying it, because a revenue meter is exactly the device someone might mistake for authoritative.

## What this repo inherits deliberately

The packaging, CI, release and review conventions are copied from `ebus-panel-sim` rather than reinvented, including several that exist because something went wrong there:

- The wheel is asserted in `publish.yml`, because that package shipped four releases before anyone noticed its wheel had never built. The test suite reads the source tree and cannot catch it.
- `py.typed` ships from the first release, because shipping a `mypy --strict` package without the marker means consumers resolve it to `Any`.
- The version is single-sourced from `__version__`, and the publish workflow refuses a tag that disagrees with it.
- `CONTRIBUTING.md` carries a definition of done, because on a published package a deferred documentation fix is a second release.
