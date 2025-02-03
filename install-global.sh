#! /bin/bash

python3 -m compileall ./
mkdir ./build
mv ./__pycache__/* ./build/steam-prefix
chmod +x ./build/steam-prefix
rm -rf ./__pycache__/
sudo cp ./build/steam-prefix /bin/steam-prefix
sudo ln /bin/steam-prefix /etc/profile.d/steam-prefix
