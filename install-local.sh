#! /bin/bash

python3 -m compileall ./
mkdir ./build
mv ./__pycache__/* ./build/steam-prefix
chmod  +x ./build/steam-prefix
rm -rf ./__pycache__/
cp ./build/steam-prefix $HOME/.local/bin/steam-prefix
echo "$HOME/.local/bin/steam-prefix > /dev/null 2>&1 &" >> $HOME/.profile
