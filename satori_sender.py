from data import login, password, test_file, problem
import requests
import argparse
import time
import re

import colorama
from colorama import Fore,Back,Style

parser = argparse.ArgumentParser(
                    prog='Satori Sender',
                    description='Sends specified file to satori. Login credentials need to be specified in data.py, also default file and problem link.')

parser.add_argument('-f', '--file', default=test_file)     # file name
parser.add_argument('-p', '--problem', default=problem)  # link to the problem
args = parser.parse_args()

parts = args.problem.split('/')
for i in range(len(parts)-1):
    if parts[i] == "contest":
        contestId = parts[i+1]
    if parts[i] == "problems":
        problemId = parts[i+1]

loginUrl = "https://satori.tcs.uj.edu.pl/login"
submitUrl = f"https://satori.tcs.uj.edu.pl/contest/{contestId}/submit"
payload = {'login': login, 'password': password}


with requests.Session() as s:
    login = s.post(loginUrl, data=payload)
    print(f'Login status: {login.status_code}')
    print("Sending a submit")
    submit = s.post(submitUrl, data={'problem': problemId}, files={'codefile':open(args.file,"rb")})
    print("Obtaining submit ID...")
    
    submitID = re.search(r'results/(.*?)"', submit.text).group(1)
    print(f"Submit ID: {Style.BRIGHT}{Fore.CYAN}{submitID}{Style.RESET_ALL}")
    resultsURL = f"https://satori.tcs.uj.edu.pl/contest/{contestId}/results/{submitID}"
    print(f"Waiting for result... {Style.DIM}{Back.YELLOW}QUE{Style.RESET_ALL} now")
    while True:
        res = s.get(resultsURL)
        status = re.search(r'<td class=sta(.*?)>', res.text).group(1)
        if status != "QUE":
            if status == "OK":
                print(f"Status: {Back.GREEN}{status}{Style.RESET_ALL} :D")
            else:
                print(f"Status: {Back.RED}{status}{Style.RESET_ALL} :c")
                
            print(resultsURL)
            break
        time.sleep(5)
