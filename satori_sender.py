from data import login, password
import requests
import argparse
import time
import re
from requests.adapters import HTTPAdapter, Retry

from colorama import Fore,Back,Style

parser = argparse.ArgumentParser(
                    prog='Satori Sender',
                    description='Sends specified file to satori. Login credentials need to be specified in data.py, also default file and problem link.')

parser.add_argument('-f', '--file', required=True)     # file name
parser.add_argument('-p', '--problem', required=True)  # link to the problem
args = parser.parse_args()

parts = args.problem.split('/')

contestId = None
problemId = None
    
for i in range(len(parts)-1):
    if parts[i] == "contest":
        contestId = parts[i+1]
    if parts[i] == "problems":
        problemId = parts[i+1]

if contestId is None or problemId is None:
    print("Error: The problem link is not correct or not specified")
    exit(1)

loginUrl = "https://satori.tcs.uj.edu.pl/login"
submitUrl = f"https://satori.tcs.uj.edu.pl/contest/{contestId}/submit"
payload = {'login': login, 'password': password}

try:
    file = open(args.file,"rb")
except OSError:
    print("Error: Given file could not be opened")
    exit(1)

with requests.Session() as s:
    adapter = HTTPAdapter(max_retries=Retry(total=10, backoff_factor=0.5))
    s.mount('https://', adapter)

    login = s.post(loginUrl, data=payload)
    print(f'Login status: {login.status_code}')
    print("Sending a submit")
    submit = s.post(submitUrl, data={'problem': problemId}, files={'codefile': file})
    file.close()


    print("Obtaining submit ID...")

    submitID = re.search(r'results/(.*?)"', submit.text).group(1)
    if submitID == None: 
        print("Error: could not obtain submit ID, exiting...")
        exit(1)
    
    print(f"Submit ID: {Style.BRIGHT}{Fore.CYAN}{submitID}{Style.RESET_ALL}")
    resultsURL = f"https://satori.tcs.uj.edu.pl/contest/{contestId}/results/{submitID}"
    print(f"Waiting for result... {Style.DIM}{Back.YELLOW}QUE{Style.RESET_ALL} now")
    while True:
        time.sleep(5)
        try:
            res = s.get(resultsURL)
            status = re.search(r'<td class=sta(.*?)>', res.text).group(1)
        except:
            print("Something went wrong")
            print(resultsURL)
            exit(1)

        if status != "QUE" and status != "None":
            if status == "OK":
                print(f"Status: {Back.GREEN}{status}{Style.RESET_ALL} :D")
            else:
                print(f"Status: {Back.RED}{status}{Style.RESET_ALL} :c")
                
            print(resultsURL)
            break
            
