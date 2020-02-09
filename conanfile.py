from conans import ConanFile, tools
from conans.tools import os_info, SystemPackageTool
import os
from conans.errors import ConanInvalidConfiguration

class ConanArduinoSDKConan(ConanFile):
    name = "arduino-sdk"
    version = "1.8.11"
    gcc_version = "7.3"
    archs = ("avr")

    license = "Mozilla Public License, v. 2.0 http://mozilla.org/MPL/2.0/"
    url = "https://github.com/Dr-QP/conan-arduino-sdk"
    description = "Conan package that installs Arduino as SDK"

    settings = "os", "compiler", "arch"
    options = {"host_os": ["linux32", "linux64", "windows", "macOS"]}

    no_copy_source = True

    sdk_source_folder = "<platform specific>"
    download_path = "<platform specific>"
    url = "<platform specific>"


    def configure(self):
        import sys
        is_64bits = sys.maxsize > 2 ** 32


        if str(self.settings.os) != "Arduino":
            self.raise_settings_error(f"OS '{self.settings.os}' is not supported, only `Arduino` supported.")
        elif str(self.settings.compiler) not in ("gcc"):
            self.raise_settings_error(f"Compiler '{self.settings.compiler}' is not supported, only gcc is available")
        elif str(self.settings.compiler.version) != self.gcc_version:
            self.raise_settings_error(f"Compiler version '{self.settings.compiler.version}' is not supported, only {self.gcc_version} is available")
        elif str(self.settings.compiler.libcxx) != 'libstdc++11':
            self.raise_settings_error(f"Compiler libcxx '{self.settings.compiler.libcxx}' is not supported, only libstdc++11 is available")
        elif str(self.settings.arch) not in self.archs:
            self.raise_settings_error(f"Architecture '{self.settings.arch}' is not supported, only {','.join(self.archs)} are available")

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
            self.sdk_source_folder = "arduino-%s" % self.version

        elif self.options.host_os == "macOS":
            self.url = "https://downloads.arduino.cc/arduino-%s-macosx.zip" % self.version
            self.download_path = "arduino-%s.zip" % self.version
            self.sdk_source_folder = os.path.join("Arduino.app", 'Contents', 'Java')

        elif self.options.host_os == "windows":
            self.url = "https://downloads.arduino.cc/arduino-%s-windows.zip" % self.version
            self.download_path = "arduino-%s.zip" % self.version
            self.sdk_source_folder = "arduino-%s" % self.version


    def raise_settings_error(self, message):
        raise ConanInvalidConfiguration(message + "\n\nValid profile looks like:\n" + self.gen_profile())

    def gen_profile(self):
        return f'''
include(default)

[settings]
os=Arduino
os.board=any
arch=avr
compiler=gcc
compiler.libcxx=libstdc++11
compiler.version={self.gcc_version}

[build_requires]
{self.name}/{self.version}@{self.user}/{self.channel}
'''

    def build_requirements(self):
        if os_info.is_linux:
            installer = SystemPackageTool()
            installer.install("xz-utils", update=True)

    def build(self):
        self.output.warn("Downloading: %s" % self.url)
        tools.download(self.url, self.download_path)

        if os_info.is_linux:
            self.run("tar xvfJ %s" % self.download_path)
        else:
            tools.unzip(self.download_path, keep_permissions=True)

    def package(self):
        self.copy("hardware/*", src=self.sdk_source_folder, keep_path=True)
        self.copy("libraries/*", src=self.sdk_source_folder, keep_path=True)
        self.copy("examples/*", src=self.sdk_source_folder, keep_path=True)

    def package_info(self):
        full_sdk_path = str(self.package_folder)
        self.env_info.CONAN_ARDUINO_SDK_PATH = full_sdk_path
        self.env_info.ARDUINO_SDK_PATH = full_sdk_path

        sys_root = os.path.join(full_sdk_path, 'hardware', 'tools', 'avr')
        bin_folder = os.path.join(sys_root, 'bin')
        self.env_info.path.append(bin_folder)
        self.env_info.CC = os.path.join(bin_folder, "avr-gcc")
        self.env_info.CXX = os.path.join(bin_folder, "avr-g++")
        self.env_info.GCOV = os.path.join(bin_folder, "avr-gcov")
        self.env_info.RANLIB = os.path.join(bin_folder, "avr-gcc-ranlib")
        self.env_info.NM = os.path.join(bin_folder, "avr-gcc-nm")

        self.env_info.AR = os.path.join(bin_folder, "avr-ar")
        self.env_info.AS = os.path.join(bin_folder, "avr-as")

        self.env_info.LD = os.path.join(bin_folder, "avr-ld")
        self.env_info.STRIP = os.path.join(bin_folder, "avr-strip")

        self.env_info.SYSROOT = sys_root
        self.env_info.CONAN_CMAKE_FIND_ROOT_PATH = sys_root
