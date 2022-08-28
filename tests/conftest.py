"""Test initialisation code run by pytest."""
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def always_allowed_dir(pytestconfig: pytest.Config) -> Path:
    """We have to always allow write access to this directory when creating rules.

    This is to allow writing to .coverage and .pytest_cache.
    """
    return pytestconfig.rootpath
