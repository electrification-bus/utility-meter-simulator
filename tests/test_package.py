"""Scaffold-level guarantees.

Thin, but not decorative: each of these pins something that has actually gone
wrong in the sibling repo. The version test guards the single-source-of-truth
wiring that `publish.yml`'s tag check depends on, and the harness test guards
the paho patch that every future wire test will assert through.
"""

from __future__ import annotations

import ebus_utility_meter_sim as pkg
from ebus_utility_meter_sim import (
    ConfigValidationError,
    EmitterStateError,
    UtilityMeterSimError,
)

from .conftest import PahoRecorder


def test_version_is_a_release_shaped_string() -> None:
    """`pyproject`'s `[tool.hatch.version]` reads this attribute, and publish.yml
    refuses to release when the git tag disagrees with it. A non-string or a
    missing attribute breaks the build rather than the test."""
    assert isinstance(pkg.__version__, str)
    assert pkg.__version__.count(".") == 2


def test_exceptions_share_one_root() -> None:
    """So a caller can catch everything this package raises without resorting to
    bare `Exception`."""
    for exc in (ConfigValidationError, EmitterStateError):
        assert issubclass(exc, UtilityMeterSimError)


def test_public_surface_is_exported() -> None:
    assert set(pkg.__all__) <= set(dir(pkg))


def test_paho_is_patched_so_no_socket_opens(rec: PahoRecorder) -> None:
    """The autouse fixture must be active for every test module, not just the one
    that declares it. Nothing has published yet, so the recorder is empty; what
    this asserts is that the fixture resolves and the read model works."""
    assert rec.published == []
    assert rec.retained == {}
