"""Tests Landlock on unsupported platforms (MacOS and Windows)."""
import platform

import pytest

from landlock import Ruleset, SyscallError


@pytest.mark.skipif(platform.system() != "Darwin", reason="requires Darwin")
def test_macos_error():
    """Test that a sensible error is raised when using landlock on MacOS."""
    with pytest.raises(SyscallError) as exec_info:
        Ruleset()
    assert (
        exec_info.value.reason
        == "Landlock is a only available on Linux, it looks like you're running Darwin"
    )


@pytest.mark.skipif(platform.system() != "Windows", reason="requires Windows")
def test_windows_error():
    """Test that a sensible error is raised when using landlock on Windows."""
    with pytest.raises(SyscallError) as exec_info:
        Ruleset()
    assert (
        exec_info.value.reason
        == "Landlock is a only available on Linux, it looks like you're running Windows"
    )
