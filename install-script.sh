#!/bin/bash

INSTALL_LOC="/usr/local/bin"
PROGAM_NAME="pyscan"

# Install program reqs.txt
python3 -m venv venv
source venv/bin/activate
pip install -r reqs.txt

# Compile python code to executable
pyinstaller "$PROGRAM_NAME".spec

# Create system wide command
sudo mv ./dist/$PROGRAM_NAME $INSTALL_LOC
sudo chmod +x $INSTALL_LOC/$PROGRAM_NAME

deactivate