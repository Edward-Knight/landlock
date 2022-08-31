"""Test initialisation code run by pytest."""
import platform
from pathlib import Path

import pytest


def pytest_configure(config):
    """Make sure that the "forked" marker is defined even on Windows.

    This stops --strict-markers from failing.
    """
    if platform.system() == "Windows":
        config.addinivalue_line(
            "markers", "forked: dummy marker - pytest-forked not available on Windows"
        )


@pytest.fixture(scope="session")
def always_allowed_dir(pytestconfig: pytest.Config) -> Path:
    """We have to always allow write access to this directory when creating rules.

    This is to allow writing to .coverage and .pytest_cache.
    """
    return pytestconfig.rootpath
