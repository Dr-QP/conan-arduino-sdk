project(PackageTest CXX)
cmake_minimum_required(VERSION 3.10.0)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(${PROJECT_NAME} example.cpp)
