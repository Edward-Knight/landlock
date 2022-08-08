from landlock.porcelain import landlock_abi_version


def main():
    abi = landlock_abi_version()
    print(f"Landlock LSM is enabled, ABI version {abi}")


if __name__ == "__main__":
    main()
