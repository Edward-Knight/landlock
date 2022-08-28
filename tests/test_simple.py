"""Some simple tests for Landlock."""
from pathlib import Path

import pytest

from landlock import Ruleset, landlock_abi_version


def test_simple_usage(always_allowed_dir: Path, tmp_path: Path):
    # test getting the Landlock ABI version
    abi = landlock_abi_version()
    print(f"Landlock LSM is enabled, ABI version {abi}")
    assert abi > 0

    # set up directories for testing
    allowed_dir = tmp_path / "allowed"
    allowed_dir.mkdir()
    assert allowed_dir.is_dir()
    disallowed_dir = tmp_path / "disallowed"
    disallowed_dir.mkdir()
    assert disallowed_dir.exists()

    def _create_file(path: Path):
        assert not path.exists()
        path.write_text("test")
        assert path.read_text() == "test"

    # test creating a file in disallowed_dir
    # this works because we haven't turned on protections yet
    _create_file(disallowed_dir / "okay")

    # test creating a ruleset
    # should disallow all filesystem access except always_allowed_dir and allowed_dir
    rs = Ruleset()
    rs.allow(always_allowed_dir)
    rs.allow(allowed_dir)
    rs.apply()

    # test creating a file in allowed_dir (should work)
    _create_file(allowed_dir / "okay")

    # test creating a file in disallowed_dir (should not work)
    with pytest.raises(PermissionError):
        _create_file(disallowed_dir / "error")
