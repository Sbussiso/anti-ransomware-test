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

print("Files to be decrypted:", files)

# Reading the key from the key file
with open("thekey.key", "rb") as key:
    secretKey = key.read()

# Decrypting all the files
for file in files:
    try:
        with open(file, "rb") as thefile:
            contents = thefile.read()
        contents_decrypted = Fernet(secretKey).decrypt(contents)
        with open(file, "wb") as thefile:
            thefile.write(contents_decrypted)
        print(f"Decrypted {file}")
    except Exception as e:
        print(f"Skipping file {file} due to {e}")

message = """Decryption process completed.\n
     _                         _
    |_|                       |_|
    | |         /^^^\         | |
   _| |_      (| "o" |)      _| |_
 _| | | | _    (_---_)    _ | | | |_ 
| | | | |' |    _| |_    | `| | | | |
\          /   /     \   \          /
 \        /  / /(. .)\ \  \        /
   \    /  / /  | . |  \ \  \    /
     \  \/ /    ||Y||    \ \/  /
       \_/      || ||      \_/
                () ()
                || ||
               ooO Ooo
"""
print(message)