from conans import ConanFile, CMake
import os

class ConanArduinoSDKTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def test(self):
        arduino_path = os.getenv("CONAN_ARDUINO_SDK_PATH")
        if not arduino_path:
            raise Exception(
                "CONAN_ARDUINO_SDK_PATH environment variable is not set")
        if not os.path.exists(arduino_path):
            raise Exception(
                "CONAN_ARDUINO_SDK_PATH folder doesn't exist: %s" % arduino_path)
                
        self.output.success("Done")
