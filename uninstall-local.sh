#! /bin/bash

rm -f $HOME/.local/bin/steam-prefix
sed -i "/steam-prefix/d" $HOME/.profile
