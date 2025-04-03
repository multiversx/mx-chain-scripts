import sys


def is_linux():
    return get_platform() == "linux"


def is_osx():
    return get_platform() == "osx"


def get_platform():
    platforms = {
        "linux": "linux",
        "linux1": "linux",
        "linux2": "linux",
        "darwin": "osx",
        "win32": "windows",
        "cygwin": "windows",
        "msys": "windows"
    }

    platform = platforms.get(sys.platform)
    if platform is None:
        raise Exception(f"Unknown platform: {sys.platform}")

    return platform
