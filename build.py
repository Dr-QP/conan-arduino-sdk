from conan.packager import ConanMultiPackager
from conans.tools import os_info
import copy

if __name__ == "__main__":
    builder = ConanMultiPackager(reference="arduino-sdk/1.8.8")
    builder.build_policy = "missing"
    builder.add()

    if os_info.is_linux:
        filtered_builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            filtered_builds.append([settings, options, env_vars, build_requires])
            new_options = copy.copy(options)
            new_options["ardiono-sdk:host_os"] = "linux32"
            filtered_builds.append([settings, new_options, env_vars, build_requires])
        builder.builds = filtered_builds

    builder.run()
