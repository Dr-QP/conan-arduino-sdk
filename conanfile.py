from conans import ConanFile, tools
from conans.tools import os_info, SystemPackageTool
import os

class ConanarduinosdkConan(ConanFile):
    name = "conan-arduino-sdk"
    version = "1.8.3"
    license = "Mozilla Public License, v. 2.0 http://mozilla.org/MPL/2.0/"
    url = "https://github.com/Dr-QP/conan-arduino-sdk"
    description = "Conan package that installs Arduino as SDK"
    settings = None
    
    app_folder = "<platform specific>"
    zip_folder = "<platform specific>"
    download_path = "<platform specific>"
    url = "<platform specific>"

    def configure(self):
        if os_info.is_linux:
            self.url = "https://downloads.arduino.cc/arduino-%s-linux64.tar.xz" % self.version
            self.download_path = "arduino-%s.tar.xz" % self.version
            self.zip_folder = "arduino-%s" % self.version
            self.app_folder = "arduino"

        if os_info.is_macos:
            self.url = "https://downloads.arduino.cc/arduino-%s-macosx.zip" % self.version
            self.download_path = "arduino-%s.zip" % self.version
            self.zip_folder = "Arduino.app"
            self.app_folder = self.zip_folder


    def system_requirements(self):
        if os_info.is_linux:
            installer = SystemPackageTool()
            installer.update()
            installer.install("openjdk-8-jre")
            installer.install("openjdk-8-jre-headless")
            installer.install("xz-utils")

    def source(self):
        self.output.warn("Downloading: %s" % self.url)
        tools.download(self.url, self.download_path)

    if os_info.is_linux:
        self.run("tar xvfJ %s" % self.download_path)
    else:
        tools.unzip(self.download_path, keep_permissions=True)

    def package(self):
        self.copy("*", dst=self.app_folder, src=self.zip_folder, keep_path=True)

    def package_info(self):
        self.env_info.CONAN_ARDUINO_SDK_PATH = str(self.package_folder)
