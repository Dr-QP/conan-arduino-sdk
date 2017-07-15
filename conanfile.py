from conans import ConanFile, tools
from conans.tools import os_info, SystemPackageTool


class ConanarduinosdkConan(ConanFile):
    name = "conan-arduino-sdk"
    version = "1.0.0"
    license = "Mozilla Public License, v. 2.0 http://mozilla.org/MPL/2.0/"
    url = "https://github.com/Dr-QP/conan-arduino-sdk"
    description = "Conan package that installs Arduino as SDK"
    settings = "os", "compiler", "build_type", "arch"
    # exports_sources = "!build/*", "!test_package/*", "!**/.DS_Store"
    options = {
        "arduino_version": ["1.8.3", "ANY", "none"],
        "arduino_path": "ANY"
    }
    default_options = "arduino_version=none", "arduino_path=none"

    def source(self):
        self.arduino_path = str(self.options.arduino_path)
        if self.options.arduino_version != "none" and self.arduino_path == "none":
            if os_info.is_linux:
                installer = SystemPackageTool()
                installer.install("openjdk-8-jre")
                installer.install("openjdk-8-jre-headless")
                installer.install("curl")
                installer.install("xz-utils")

                self.run("curl https://downloads.arduino.cc/arduino-%s-linux64.tar.xz -o /tmp/arduino.tar.xz" %
                         self.options.arduino_version)
                self.run("tar xvfJ /tmp/arduino.tar.xz")

                self.output.warn("Downloading: %s" % url)
                tools.download(url, dest_file)
                tools.unzip(dest_file)

                self.arduino_path = "/tmp/arduino-%s/" % self.options.arduino_version
                self.run("%s/install.sh" % self.arduino_path)


    # def package(self):
    #     self.copy("*.h", dst="include", src="src")
    #     self.copy("*.lib", dst="lib", keep_path=False)
    #     self.copy("*.dll", dst="bin", keep_path=False)
    #     self.copy("*.dylib*", dst="lib", keep_path=False)
    #     self.copy("*.so", dst="lib", keep_path=False)
    #     self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]
