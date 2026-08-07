"""Public exception hierarchy for ebus-utility-meter-sim.

One root so a caller can catch everything this package raises without catching
``Exception``, and distinct leaves so the common producer-side mistakes are
distinguishable at the call site rather than by matching message text.
"""

from __future__ import annotations


class UtilityMeterSimError(Exception):
    """Root of every error this package raises."""


class ConfigValidationError(UtilityMeterSimError):
    """The meter configuration is missing a required field, or a field's value is
    not usable (wrong type, out of range, or an enum value the spec does not
    define). Raised at construction rather than at first publish, so a malformed
    config fails before anything reaches the broker."""


class EmitterStateError(UtilityMeterSimError):
    """A producer-side lifecycle mistake: publishing before ``start()``, passing
    two answers to which connection to publish through, or addressing an instance
    that was never configured."""
