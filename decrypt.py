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




with open("thekey.key", "rb") as key:
        secretKey = key.read()


for file in files:
        with open(file, "rb") as thefile:
                contents = thefile.read()
        contents_decrypted = Fernet(secretKey).decrypt(contents)
        with open(file, "wb") as thefile:
                thefile.write(contents_decrypted)