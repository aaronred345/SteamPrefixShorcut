#! /bin/bash

python3 -m compileall ./
mkdir ./build
mv ./__pycache__/* ./build/steam-prefix
chmod +x ./build/steam-prefix
rm -rf ./__pycache__/
sudo cp ./build/steam-prefix /bin/steam-prefix
echo "/bin/steam-prefix > /dev/null 2>&1 &" > ./steam-prefix.sh
sudo mv ./steam-prefix.sh /etc/profile.d/steam-prefix.sh
