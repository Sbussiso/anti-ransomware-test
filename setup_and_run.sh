#!/bin/bash

# Function to check if the script is run as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo "This script must be run as root. Re-running with sudo..."
        sudo "$0" "$@"
        exit $?
    fi
}

# Function to install system dependencies
install_dependencies() {
    echo "Updating package list and installing dependencies..."
    sudo apt update
    sudo apt install python3 python3-venv python3-pip -y
}

# Function to set up the virtual environment and install Python dependencies
setup_virtualenv() {
    echo "Setting up the virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install cryptography
}

# Function to run the main Python script
run_main_script() {
    echo "Running the main Python script..."
    source venv/bin/activate
    python3 main.py
}

# Main script execution
main() {
    check_root
    install_dependencies
    setup_virtualenv
    run_main_script
}

main "$@"
