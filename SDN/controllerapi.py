# coding:utf-8

import json
import base64
import http.client
from http_post import http_post
def pre_get(urls):
    try:
        url = urls
        str='admin' + ':' + 'admin'
        auth = base64.b64encode(str.encode())
        headers = {"Authorization": "Basic " + auth.decode(), "Content-Type": "application/json"}
        conn = http.client.HTTPConnection('127.0.0.1:8181', timeout=3)
        conn.request(method="GET", url=url, headers=headers)
        response = conn.getresponse()
        ret = response.read()
        return {"status": 1, "data": ret}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": 0}


def pre_put(url, body):
    try:
        strs = 'admin' + ':' + 'admin'
        auth = base64.b64encode(strs.encode())
        headers = {"Authorization": "Basic " + auth.decode(), "Content-Type": "application/json"}
        conn = http.client.HTTPConnection('127.0.0.1:8181', timeout=3)
        conn.request(method="PUT",url=url,body=body,headers=headers)
        response = conn.getresponse()
        ret=response.read()
        print(response.status)
        if response.status in [200, 201]:
            return "add success"
        else:
            return 'add failure'

    except Exception as e:
        import traceback
        traceback.print_exc()
        return 'add failure'

def pre_post(url,body):
    try:
        strs = 'admin' + ':' + 'admin'
        auth = base64.b64encode(strs.encode())
        headers = {"Authorization": "Basic " + auth.decode(), "Content-Type": "application/json"}
        conn = http.client.HTTPConnection('127.0.0.1:8181', timeout=3)
        conn.request(method="POST",url=url,body=body,headers=headers)
        response = conn.getresponse()
        ret=response.read()
        print(response.status)
        if response.status in [200, 201]:
            return "add success"
        else:
            return 'add failure'
    except Exception as e:
        import traceback
        traceback.print_exc()
        return 'add failure'

def add_meter(swid,meterid,size,lim,rate):
    switch_id = "openflow:231225997531456"
    url = "http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/" + swid + "/meter/"+meterid

    meter_id = {"meter-id": meterid}
    meter_header = {"meter-band-headers": {
        "meter-band-header": {
            "band-id": "0",
            "band-rate": rate,
            "band-burst-size": size,
            "meter-band-types": {"flags": "ofpmbt-drop"},
            "drop-burst-size": "0",
            "drop-rate": lim
        }
    }
    }

    meter_name = {"meter-name": "guestMeter"}
    meter_container_name = {"container-name": "guestMeterContainer"}
    meter_flags = {"flags": "meter-kbps"}

    meter_set = {}
    meter_set.update(meter_id)
    meter_set.update(meter_header)
    meter_set.update(meter_name)
    meter_set.update(meter_container_name)
    meter_set.update(meter_flags)

    body = json.dumps({"meter": meter_set})
    print(body)
    pre_put(url, body)

def _process_operation_flows(data):
    resp_data=[]
    data=json.loads(data)
    if "nodes" in data:
        nodes=data['nodes']
        if "node" in nodes:
            for node in nodes['node']:
                resp_node=dict()
                resp_node['id']=node['id']
                if "flow-node-inventory:table" in node:
                    for table in node['flow-node-inventory:table']:
                        if "flow" in table:
                            resp_node["flows"]=table['flow']
                resp_data.append(resp_node)
    return resp_data

def _process_operation_meter(data):
    resp_data=[]
    data=json.loads(data)
    if "nodes" in data:
        nodes=data['nodes']
        if "node" in nodes:
            for node in nodes['node']:
                if "flow-node-inventory:meter" in node:
                    for meter in node['flow-node-inventory:meter']:
                        meter_band=meter['meter-band-headers']['meter-band-header'][0]
                        resp_node=dict(
                            id=meter['meter-id'],
                            name=meter['meter-name'],
                            flags=meter['flags'],
                            rate=meter_band['band-rate'],
                            burst_size=meter_band['band-burst-size'],
                            type=meter_band['meter-band-types']['flags']
                        )
                        resp_data.append(resp_node)
    return resp_data

def list_flows():
    res=dict()
    url="/restconf/operational/opendaylight-inventory:nodes"
    reply=pre_get(url)
    if reply['status']:
        reply_data=reply['data']
        if reply_data:
            res['status']='success'
            res['data']=_process_operation_flows(reply_data)
        else:
            res['status']='error'
            res['reason']="连接控制器失败"
    else:
        res['status'] = 'error'
        res['reason'] = "连接控制器失败"
    return res

def flow_delete(switch_id,flow_id):
    url_in = "/restconf/config/opendaylight-inventory:nodes/node/" + switch_id + "/flow-node-inventory:table/0/flow/"+flow_id
    auth = base64.b64encode('admin:admin'.encode())
    headers = {"Authorization": "Basic " + auth.decode(), "Content-Type": "application/json"}
    conn = http.client.HTTPConnection('127.0.0.1:8181', timeout=3)
    try:
        conn.request("DELETE", url_in, json.dumps({}), headers)
    except:
        import traceback
        traceback.print_exc()

def add_flow(sw_id,flow_id,flow):
    url="/restconf/config/opendaylight-inventory:nodes/node/" + sw_id + "/flow-node-inventory:table/0/flow/"+flow_id
    ref=pre_put(url,flow)
    return ref

def add_qos(body):
    url="/restconf/operations/qos-flow:add-qos-config"
    ref=pre_post(url,body)
    return ref

def list_meter():
    res=dict()
    url="/restconf/config/opendaylight-inventory:nodes"
    reply=pre_get(url)
    if reply['status']:
        reply_data=reply['data']
        if reply_data:
            res['status']='success'
            res['data']=_process_operation_meter(reply_data)
        else:
            res['status']='error'
            res['reason']="连接控制器失败"
    else:
        res['status'] = 'error'
        res['reason'] = "连接控制器失败"
    return res


