import json
from http_post import http_post
file_in = open('test.json','r', encoding='UTF-8')
url="http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:1/flow-node-inventory:table/0/flow/flow1"
file_data=json.load(file_in)
file=json.dumps(file_data)
http_post(url,file)
file_in.close()


