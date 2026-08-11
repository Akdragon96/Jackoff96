import argparse 
import hashlib
parse=argparse.ArgumentParser(description="This simple tool will help to crack the hashes")
parse.add_argument('-w','--wordlist',type=str,help="wordlist for guesses",required=True)
parse.add_argument('-t','--hashtype',type=str,help="type of algorithms used",required=True)
parse.add_argument('-s','--hashstr',type=str,help="insert hash here ",required=True)
arg=parse.parse_args()
if arg.hashtype not in hashlib.algorithms_guaranteed:
    print("incorrect data is being used here")
    exit()
    
#important 
hash_func=getattr(hashlib,arg.hashtype)
try:
    with open(arg.wordlist,'r',encoding='utf-8',errors='ignore') as f:
        for line in f:
            word=line.strip()
            if hash_func(word.encode()).hexdigest()==arg.hashstr:
                print("match found", word)
                break

        else:
            print("No match found in wordlist")
except FileNotFoundError:
    print(f"wordlist file not found: {arg.wordlist}")
finally:
    print("Thankyou for using our tool")


