#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew update
    brew upgrade python3
elif [[ "$TRAVIS_OS_NAME" == "windows" ]]; then
    choco install python3 --params "/InstallDir:/c/python3"
fi

if [[ "$TRAVIS_OS_NAME" == "windows" ]]; then
    export PATH="$PATH:/c/python3/bin"
    tree /c/python3
fi

pip3 install conan conan_package_tools --upgrade

conan user
