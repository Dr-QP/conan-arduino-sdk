#!/bin/bash

set -e
set -x

# if [[ "$(uname -s)" == 'Darwin' ]]; then
#     brew update
#     brew upgrade python3
# fi

pip3 install conan conan_package_tools --upgrade

conan user
