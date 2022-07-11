import os
from cryptography.fernet import Fernet

affected_files = []
direct = []
with open("start_dir.txt", "w") as f:
    f.write(os.getcwd())
with open("start_dir.txt", "r") as f:
    start_dir = f.read()
os.remove("start_dir.txt")

direct = []
def get_files_in_direct():

    os.chdir(start_dir)
    
    for file in os.listdir():
        if file == "ransom.py" or file == "ransom.py.bak" or file == "thekey.key" or file == "decrypt.py.bak" or file == "decrypt.py":
            continue
        if os.path.isfile(file):
            affected_files.append(file)
        elif os.path.isdir(file):
            direct.append(file)  

    for directory in direct:
        os.chdir(directory)
        for file in os.listdir():
            if os.path.isfile(file):
                affected_files.append(file)
            if os.path.isdir(file):
                direct.append(file)
    os.chdir(start_dir)
    
get_files_in_direct()

direct.append(start_dir)

with open("thekey.key", "rb") as thekey:
    key = thekey.read()

for d in direct:
    os.chdir(d)
    for file in os.listdir():
        if file in affected_files:
            with open(file, "rb") as thefile:
                cont = thefile.read()
            decr_cont = Fernet(key).decrypt(cont)
            with open(file, "wb") as thefile:
                thefile.write(decr_cont)
        else: 
            continue
            
