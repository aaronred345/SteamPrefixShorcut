## About
This is a tool to create easy to find, named by the game, symbolic links to proton/wine prefixes for Steam games.
It will search through your home directory to find location of steam installation. If there are multiple, it will ask you which one (or all of them) you want to use

You can either run this as a normal python script with `python3 main.py` or install it onto your machine so you can call it from the command line anywhere, as well as running on login.
Installing globally requires sudo, installing localy doesn't as it's just installing it into your home directory

### Requirements
 - python3
 - c compiler, only tested with gcc (Only needed if using install scripts)

### To Install
`chmod +x *.sh`

`./install-global.sh` OR `./install-local.sh`

### To Uninstall
`./uninstall-global.sh` OR `./uninstall-local.sh` (Depending on which one you used to install)
