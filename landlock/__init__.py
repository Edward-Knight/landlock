"""Python interface to the Landlock Linux Security Module."""

__version__ = "0.0.0dev0"


class LandlockError(Exception):
    """Generic exception for this module."""


class SyscallError(Exception):
    """Exception raised from libc syscall."""
