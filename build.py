from conan.packager import ConanMultiPackager
from conans.tools import os_info

if __name__ == "__main__":
    builder = ConanMultiPackager(args="--build missing", username="anton-matosov", channel="stable")
    builder.add(options={
        "conan-ardiono-sdk:use_bundled_java": False
    })
    if os_info.is_linux or os_info.is_windows:
        builder.add(options={
            "conan-ardiono-sdk:use_bundled_java": True
        })

    builder.run()
