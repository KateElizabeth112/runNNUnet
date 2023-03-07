#!/bin/bash

# Launch virtual environment
source venv/bin/activate

# Install pytorch
pip3 install torch torchvision

# Install nnUNet
pip3 install --upgrade setuptools
pip3 install git+https://github.com/KateElizabeth112/nnUnet.git