#!/bin/bash

# Ensure the script is being run with sudo on Linux
if [ "$(uname -s)" = "Linux" ] && [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root. Re-running with sudo..."
    exec sudo "$0" "$@"
fi

# Set up virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install necessary packages
pip install cryptography

# Run the encryption script
python main.py
