import requests
from requests.auth import HTTPBasicAuth

# Simple authenticated POST helper for controller debugging scripts.

def http_post(url,jstr):
    url= url
    headers = {'Content-Type':'application/json'}
    resp = requests.post(url,jstr,headers=headers,auth=HTTPBasicAuth('admin', 'admin'))
    print(resp)
