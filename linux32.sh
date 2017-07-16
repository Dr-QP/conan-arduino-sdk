
apt update
apt install sudo git curl python build-essential libssl-dev libffi-dev python-dev

curl -O https://bootstrap.pypa.io/get-pip.py
python get-pip.py

git clone -b develop https://github.com/Dr-QP/conan-arduino-sdk.git
cd conan-arduino-sdk



conan remote add general https://api.bintray.com/conan/anton-matosov/general

conan upload conan-arduino-sdk/1.8.3/anton-matosov/stable --all -r=general


chmod +x .travis/install.sh
./.travis/install.sh

chmod +x .travis/run.sh
./.travis/run.sh
