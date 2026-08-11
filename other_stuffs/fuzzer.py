import argparse
import requests
arg=argparse.ArgumentParser(description="This argument parser is being made by me ")
arg.add_argument('-u','--url',type=str,help="Url name should be there",required=True)
arg.add_argument('-w','--wordlist',type=str,help="Enter the wordlist ",required=True)
arg.add_argument('-v','--verbose',action='store_true',help="Enables verbose mode")
parse=arg.parse_args()
file=open(parse.wordlist,'r')
words=file.read()
domain=words.split()
file.close()
print("""
        ΓûêΓûÇΓûäΓÇâΓûêΓÇâΓûêΓûÇΓûÇΓÇâΓûêΓûÇΓûÇΓÇâΓûäΓûÇΓûêΓÇâΓûêΓÇâΓûêΓûä ΓûêΓÇâΓûêΓûÇΓûÇ
        ΓûêΓûäΓûÇΓÇâΓûêΓÇâΓûêΓûäΓûäΓÇâΓûêΓûäΓûäΓÇâΓûêΓûÇΓûêΓÇâΓûêΓÇâΓûê ΓûÇΓûêΓÇâΓûêΓûäΓûê

      Subdomain Enumeration Tool
""")
for i in domain:
    try:
        res=requests.get(f"https://{i}.{parse.url}")
        if res.status_code==200:
            print(f"domain got: {i}.{parse.url}")
        else:
            print(f"{i}.{parse.url} is invalid domain")
    except Exception as e:
        if parse.verbose:
            print("unexpected error",e)