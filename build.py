from conan.packager import ConanMultiPackager
from conans.tools import os_info
import copy

if __name__ == "__main__":
    builder = ConanMultiPackager(build_policy="outdated")
    settings = {
        "os": "Arduino",
        "os.board": "any",
        "compiler": "gcc",
        "compiler.version": "7.3",
        "compiler.libcxx": "libstdc++11",
        "arch": "avr"
    }

    if os_info.is_linux:
        builder.add(settings, options={"arduino-sdk:host_os": "linux32"})
        builder.add(settings, options={"arduino-sdk:host_os": "linux64"})
    else:
        builder.add(settings)

    builder.run()
