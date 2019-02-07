import random
import os
import string
import time
import sys

path = os.path.dirname(os.path.abspath(__file__))

def clear():
    os.system('cls||clear')

def crypt_block(data, key):
    rtn = b''
    for (d,k) in zip(data,key):
        rtn += (d^k).to_bytes(1,"big")
    return rtn

def crypt_file(filename, key, mode):
    key = key.encode()
    source = open(filename, "rb")
    print ("Working on " + filename + "...")
    if mode == 'd':
        extension = (source.readline().rstrip())
        k = key * (1+(len(extension)//len(key)))
        extension = crypt_block(extension,k).decode()
    else:
        extension = "xor"
    (path,file) = os.path.split(filename)
    (name, ext) = file.rsplit(".",1)
    target = open(os.path.join(path, name + "." + extension), "wb")
    if mode == 'e':
        k = key * (1+(len(extension)//len(key)))
        ext = crypt_block(ext.encode(),k)
        target.write(ext)
        target.write(b"\n")
    data = source.read(len(key))
    while data:
        encrypted = crypt_block(data,key)
        target.write(encrypted)
        data = source.read(len(key))
    if mode == 'e':
        print("Encrypted file: " + filename)
    else:
        print("Decrypted file: " + filename)
    source.close()
    target.close()
    os.remove(filename)

def crypt_folder(p,key,mode):
    for f in os.listdir(p):
        f = os.path.join(p,f)
        if os.path.isfile(f):
            crypt_file(f,key,mode)
        else:
            crypt_folder(f,key,mode)


clear()
mode = input("Press e to encrypt and d to decrypt\n")
while mode != 'e' and mode != 'd':
    clear()
    mode = input("Press e to encrypt and d to decrypt\n")

key = ''

if mode == 'e':
    choice = input("Would you like to have a key randomly generated? (Random generation is more secure) Y or N\n")
    while choice != 'n' and choice != 'N' and choice != 'y' and choice != 'Y':
        choice = input("Would you like to have a key randomly generated? (Random generation is more secure) Y or N\n")
    if choice.lower() == 'y':
        key_length = input("How long would you like the encryption key to be?\n")
        while not key_length.isdigit():
            key_length = input("How long would you like the encryption key to be? Please enter a number\n")
        key = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(int(key_length)))
        print ("Your key is " + key + "\nPlease remember it")
    else:
        key = input("Please enter the key you wish to use\n")
elif mode == 'd':
    key = input("Please enter your key\n")
if mode == 'e':
    source = input("Please enter the name of the file or folder to encrypt\n")
else:
    source = input("Please enter the name of the file or folder to decrypt\n")
while not os.path.exists(source):
    source = input("File or folder not found. Please try again\n")
if os.path.isfile(source):
    p = os.path.join(path, source)
    crypt_file(p, key, mode)
elif os.path.isdir(source):
    path = os.path.join(path, source)
    crypt_folder(path,key,mode)
print("Exiting...")
time.sleep(1)
clear()
exit()