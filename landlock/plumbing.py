"""Landlock constants and syscalls."""
import ctypes
import enum
import functools
import os
import typing
import _ctypes

from landlock import SyscallError


CREATE_RULESET_VERSION = 1 << 0

SYSCALL_CREATE_RULESET = 444
SYSCALL_ADD_RULE = 445
SYSCALL_RESTRICT_SELF = 446


class AccessFS(enum.IntFlag):
    """These flags enable to restrict a sandboxed process to a set of actions on files and directories.

    Files or directories opened before the sandboxing are not subject to these restrictions.
    """

    # A file can only receive these access rights:
    EXECUTE = 1 << 0
    """Execute a file."""
    WRITE_FILE = 1 << 1
    """Open a file with write access."""
    READ_FILE = 1 << 2
    """Open a file with read access."""

    # A directory can receive access rights related to files or directories.
    # The following access right is applied to the directory itself, and the directories beneath it:
    READ_DIR = 1 << 3
    """Open a directory or list its content."""

    # However, the following access rights only apply to the content of a directory, not the directory itself:
    REMOVE_DIR = 1 << 4
    """Remove an empty directory or rename one."""
    REMOVE_FILE = 1 << 5
    """Unlink (or rename) a file."""
    MAKE_CHAR = 1 << 6
    """Create (or rename or link) a character device."""
    MAKE_DIR = 1 << 7
    """Create (or rename) a directory."""
    MAKE_REG = 1 << 8
    """Create (or rename or link) a regular file."""
    MAKE_SOCK = 1 << 9
    """Create (or rename or link) a UNIX domain socket."""
    MAKE_FIFO = 1 << 10
    """Create (or rename or link) a named pipe."""
    MAKE_BLOCK = 1 << 11
    """Create (or rename or link) a block device."""
    MAKE_SYM = 1 << 12
    """Create (or rename or link) a symbolic link."""
    REFER = 1 << 13
    """Link or rename a file from or to a different directory (i.e. reparent a file hierarchy)."""


class RulesetAttr(ctypes.Structure):
    _fields_ = [("handled_access_fs", ctypes.c_uint64)]


def syscall_error(result, func: _ctypes.CFuncPtr, arguments: typing.Tuple):
    errno = ctypes.get_errno()
    if errno == 0:
        return result
    name = getattr(func, "name", func.__name__)
    raise SyscallError(
        f"Error calling {name}: {func.__name__}({arguments}) = {result}"
    ) from OSError(errno, os.strerror(errno))


libc = ctypes.CDLL(None, use_errno=True)

_create_ruleset = functools.partial(libc["syscall"], SYSCALL_CREATE_RULESET)
_create_ruleset.func.name = "landlock_create_ruleset"
_create_ruleset.func.argtypes = (
    ctypes.c_long,
    ctypes.POINTER(RulesetAttr),
    ctypes.c_size_t,
    ctypes.c_uint32,
)
_create_ruleset.func.errcheck = syscall_error
_create_ruleset.func.restype = ctypes.c_long
