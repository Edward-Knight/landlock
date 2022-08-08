from landlock.plumbing import _create_ruleset, CREATE_RULESET_VERSION


def landlock_abi_version() -> int:
    return _create_ruleset(None, 0, CREATE_RULESET_VERSION)
