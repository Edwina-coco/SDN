import requests
from requests.auth import HTTPBasicAuth
def http_post(url,jstr):
    url= url
    headers = {'Content-Type':'application/json'}
    resp = requests.post(url,jstr,headers=headers,auth=HTTPBasicAuth('admin', 'admin'))
    print(resp)