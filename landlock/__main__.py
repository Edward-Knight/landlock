from os.path import expanduser

from landlock import FSAccess, Ruleset
from landlock.plumbing import landlock_abi_version


def main():
    abi = landlock_abi_version()
    print(f"Landlock LSM is enabled, ABI version {abi}")
    rs = Ruleset()
    rs.allow("/tmp", FSAccess.all())
    rs.apply()
    with open("/tmp/test", "w") as f:
        f.write("test")
    with open(expanduser("~/test"), "w") as f:
        f.write("test")


if __name__ == "__main__":
    main()
