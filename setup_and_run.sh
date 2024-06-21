#!/bin/bash

# Function to check if the script is run as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo "This script must be run as root. Re-running with sudo..."
        sudo "$0" "$@"
        exit $?
    fi
}

check_root

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required Python packages
pip install --upgrade pip setuptools wheel
pip install cryptography

# Ensure the main.py script is executable
chmod +x main.py

# Run the main.py script
python main.py
