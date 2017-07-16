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
    options = {"host_os": ["Linux", "Windows", "MacOS"],
               "host_arch": ["x86", "x86_64"],
               "use_bundled_java": [True, False]}
    default_options = "use_bundled_java=False"

    app_folder = "<platform specific>"
    zip_folder = "<platform specific>"
    download_path = "<platform specific>"
    url = "<platform specific>"

    def configure(self):
        if os_info.is_linux:
            self.options.host_os = "Linux"
        elif os_info.is_windows:
            self.options.host_os = "Windows"
        elif os_info.is_macos:
            self.options.host_os = "MacOS"
        else:
            raise Exception("Unsupported platform")

        import sys
        is_64bits = sys.maxsize > 2 ** 32
        if is_64bits:
            self.options.host_arch = "x86_64"
        else:
            self.options.host_arch = "x86"

        if os_info.is_linux:
            if is_64bits:
                self.url = "https://downloads.arduino.cc/arduino-%s-linux64.tar.xz" % self.version
            else:
                self.url = "https://downloads.arduino.cc/arduino-%s-linux32.tar.xz" % self.version
            self.download_path = "arduino-%s.tar.gz" % self.version
            self.zip_folder = "arduino-%s" % self.version
            self.app_folder = "arduino"

        elif os_info.is_macos:
            self.url = "https://downloads.arduino.cc/arduino-%s-macosx.zip" % self.version
            self.download_path = "arduino-%s.zip" % self.version
            self.zip_folder = "Arduino.app"
            self.app_folder = self.zip_folder

        elif os_info.is_windows:
            self.url = "https://downloads.arduino.cc/arduino-%s-windows.zip" % self.version
            self.download_path = "arduino-%s.zip" % self.version
            self.zip_folder = "arduino-%s" % self.version
            self.app_folder = "arduino"


    def system_requirements(self):
        if os_info.is_linux:
            installer = SystemPackageTool()
            installer.update()
            # installer.install("openjdk-8-jre")
            # installer.install("openjdk-8-jre-headless")
            installer.install("xz-utils")

    def source(self):
        self.output.warn("Downloading: %s" % self.url)
        # import shutil
        # shutil.copy2("/Users/antonmatosov/Downloads/arduino-1.8.3-linux64.tar.xz", self.download_path)
        tools.download(self.url, self.download_path)
        
        if os_info.is_linux:
            self.run("tar xvfJ %s" % self.download_path)
        else:
            tools.unzip(self.download_path, keep_permissions=True)

    def package(self):
        self.copy("*", dst=self.app_folder, src=self.zip_folder, keep_path=True)

    def package_info(self):
        self.env_info.CONAN_ARDUINO_SDK_PATH = str(self.package_folder)
        if self.options.use_bundled_java:
            self.env_info.JAVA_HOME = os.path.join(self.package_folder, "java")
            self.env_info.PATH.append(os.path.join(self.env_info.JAVA_HOME, "bin"))
