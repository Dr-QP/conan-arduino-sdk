from conans import ConanFile, tools
from conans.tools import os_info, SystemPackageTool
import os


class ConanarduinosdkConan(ConanFile):
    name = "arduino-sdk"
    version = "1.8.3"
    license = "Mozilla Public License, v. 2.0 http://mozilla.org/MPL/2.0/"
    url = "https://github.com/Dr-QP/conan-arduino-sdk"
    description = "Conan package that installs Arduino as SDK"
    settings = None
    options = {"host_os": ["linux32", "linux64", "windows", "macOS"]}
    short_paths = True

    app_folder = "<platform specific>"
    zip_folder = "<platform specific>"
    download_path = "<platform specific>"
    url = "<platform specific>"

    def configure(self):
        import sys
        is_64bits = sys.maxsize > 2 ** 32

        if self.options.host_os == None:
            if os_info.is_linux:
                if is_64bits:
                    self.options.host_os = "linux64"
                else:
                    self.options.host_os = "linux32"
            elif os_info.is_windows:
                self.options.host_os = "windows"
            elif os_info.is_macos:
                self.options.host_os = "macOS"
            else:
                raise Exception("Unsupported platform")

        if self.options.host_os in ("linux64", "linux32"):
            self.url = "https://downloads.arduino.cc/arduino-%s-%s.tar.xz" % (
                self.version, self.options.host_os)
            self.download_path = "arduino-%s.tar.gz" % self.version
            self.zip_folder = "arduino-%s" % self.version
            self.app_folder = "arduino"

        elif self.options.host_os == "macOS":
            self.url = "https://downloads.arduino.cc/arduino-%s-macosx.zip" % self.version
            self.download_path = "arduino-%s.zip" % self.version
            self.zip_folder = "Arduino.app"
            self.app_folder = self.zip_folder

        elif self.options.host_os == "windows":
            self.url = "https://downloads.arduino.cc/arduino-%s-windows.zip" % self.version
            self.download_path = "arduino-%s.zip" % self.version
            self.zip_folder = "arduino-%s" % self.version
            self.app_folder = "arduino"

    def build_requirements(self):
        if os_info.is_linux:
            installer = SystemPackageTool()
            installer.install("xz-utils", update=True)

    def source(self):
        self.output.warn("Downloading: %s" % self.url)
        tools.download(self.url, self.download_path)

        if os_info.is_linux:
            self.run("tar xvfJ %s" % self.download_path)
        else:
            tools.unzip(self.download_path, keep_permissions=True)

    def package(self):
        self.copy("*", dst=self.app_folder,
                  src=self.zip_folder, keep_path=True)

    def package_info(self):
        self.env_info.CONAN_ARDUINO_SDK_PATH = str(self.package_folder)
