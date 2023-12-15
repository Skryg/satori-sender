# Satori Sender
This utility is intended for IT Analyst students at Jagiellonian University.
Sends submits to [Satori Testing System](https://satori.tcs.uj.edu.pl/)

### Installation (Linux)
1. Make sure you have `Python 3.8` installed and `requests 2.22.0`, `colorama 0.4.3` libraries
1. Clone the repository
2. In repository directory create `data.py` file and set your Satori login credentials to `login` and `password` variables.
3. Navigate to your home directory and open `.bashrc`.
4. Add `alias satori='python3 <REPOSITORY_PATH>/satori_sender.py'` to `.bashrc`
5. Reload terminal

### Usage
If you want to send a submit simply write 
`satori -p <PROBLEM_LINK> -f <FILE>`, e.g. 
```
satori -p https://satori.tcs.uj.edu.pl/contest/7776385/problems/7829323 -f solution.cpp
```
