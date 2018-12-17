#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew update
    brew install python3
fi

pip install conan conan_package_tools --upgrade

conan user
