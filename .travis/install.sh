#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew update
    brew install conan python3
else
    pip install conan conan_package_tools --upgrade
fi

conan user
