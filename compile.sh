#! /bin/bash

python3 -m venv .venv
source ./.venv/bin/activate
python3 -m pip install nuitka
python3 -m nuitka main.py
rm -rf .venv
