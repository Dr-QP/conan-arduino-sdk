from conans import ConanFile, CMake
import os


channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "anton-matosov")


class ConanarduinosdkTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "conan-arduino-sdk/1.8.3@%s/%s" % (username, channel)


    def test(self):
        self.output.success("Done")
