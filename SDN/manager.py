from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
import sql
from flask import session
from flask import redirect
import pycurl
from io import BytesIO
from bs4 import BeautifulSoup
import json
from topologyTable import topologyTable
from flowTable import flowTable
from http_post import http_post
import requests
import topologyTable1
import controllerapi

def topologySave():
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.USERNAME, 'admin')
    c.setopt(c.PASSWORD, 'admin')
    c.setopt(c.HTTPHEADER, ["Accept:application/xml"])
    c.setopt(c.URL, 'http://127.0.0.1:8181/restconf/operational/network-topology:network-topology')
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    # jjjj测试推送
    body = buffer.getvalue()
    soup = BeautifulSoup(str(body, encoding="utf-8"))
    HostTable = []
    ip = soup.find_all('ip')
    for i in range(0, len(ip)):
        ss = BeautifulSoup(str(ip[i]))
        host = topologyTable()
        host.DDeviceIP = str(ss.get_text())
        HostTable.append(host)

    mac = soup.find_all('mac')
    for i in range(0, len(mac)):
        ss = BeautifulSoup(str(mac[i]))
        HostTable[i].DDeviceID = "host:"+str(ss.get_text())

    #取出原始的各项数据
    LinkTable = []
    s_tp = soup.find_all('source-tp')
    s_node = soup.find_all('source-node')
    d_tp = soup.find_all('dest-tp')
    d_node = soup.find_all('dest-node')
    for i in range(0, len(s_tp)):
        ss = BeautifulSoup(str(s_tp[i]))
        link = topologyTable()
        link.openflowSPort = str(ss.get_text())
        LinkTable.append(link)
    for i in range(0, len(d_tp)):
        ss = BeautifulSoup(str(d_tp[i]))
        LinkTable[i].openflowDPort = str(ss.get_text())
    for i in range(0, len(s_node)):
        ss = BeautifulSoup(str(s_node[i]))
        LinkTable[i].openflowID = str(ss.get_text())
    for i in range(0, len(d_node)):
        ss = BeautifulSoup(str(d_node[i]))
        LinkTable[i].DDeviceID = str(ss.get_text())

    #去除openflow为host的无效数据
    for l in LinkTable:
        if l.openflowID.find('host') == 0:
            LinkTable.remove(l)
    for l in LinkTable:
        if l.openflowID.find('host') == 0:
            LinkTable.remove(l)
    for l in LinkTable:
        if l.openflowID.find('host') == 0:
            LinkTable.remove(l)
    for l in LinkTable:
        if l.openflowID.find('host') == 0:
            LinkTable.remove(l)

    #为host添加IP
    for l in LinkTable:
        for h in HostTable:
            if h.DDeviceID == l.DDeviceID:
                l.DDeviceIP = h.DDeviceIP

    #修补openflow:1的link不全的bug
    for l in LinkTable:
        if l.DDeviceID == 'openflow:1':
            ll = topologyTable()
            ll.openflowID = l.DDeviceID
            ll.DDeviceID = l.openflowID
            ll.openflowSPort = l.openflowDPort
            ll.openflowDPort = l.openflowSPort
            LinkTable.append(ll)

    #按openflowID对列表排序
    for i in range(0, len(LinkTable)):
        for j in range(0, len(LinkTable)):
            if LinkTable[i].openflowID < LinkTable[j].openflowID:
                LinkTable[i], LinkTable[j] = LinkTable[j], LinkTable[i]

    #openflowID相同，按源端口对列表排序
    for i in range(0, len(LinkTable)):
        for j in range(0, len(LinkTable)):
            if LinkTable[i].openflowSPort < LinkTable[j].openflowSPort:
                if LinkTable[i].openflowID == LinkTable[j].openflowID:
                    LinkTable[i], LinkTable[j] = LinkTable[j], LinkTable[i]

    Links = []
    for l in range(0, len(LinkTable)):
        Links.append(LinkTable[l].openflowID)
        Links.append(LinkTable[l].DDeviceID)

    for i in range(0, len(Links)-1):
        if len(Links) <= i:
            break
        for j in range(i+1, len(Links)):
            if len(Links) <= j:
                break
            if Links[i] == Links[j] and Links[i+1] == Links[j-1] and (j-i) % 2 == 1 and i % 2 == 0:
                del Links[j]
                del Links[j-1]

    #去除重复的openflowID
    for i in range(1, len(LinkTable)):
        if LinkTable[len(LinkTable)-i].openflowID == LinkTable[len(LinkTable)-i-1].openflowID:
            LinkTable[len(LinkTable)-i].openflowID = ''
    #SPort，DPort修改
    for l in LinkTable:
        ss = l.openflowSPort
        l.openflowSPort = ss[-1]
        if l.openflowDPort.find('openflow') == 0:
            ss = l.openflowDPort
            l.openflowDPort = ss[-1]
        else:
            l.openflowDPort = '1'

    Openflows = []
    for l in LinkTable:
        if l.openflowID != "":
            Openflows.append(l.openflowID)
    Hosts = []
    for l in LinkTable:
        if l.DDeviceIP != "无":
            Hosts.append(l.DDeviceID)
    LinkTables=[]
    LinkTables.append(LinkTable[0])
    for i in range(1,len(LinkTable)):
        if LinkTable[i].DDeviceID!=LinkTable[i-1].DDeviceID:
            LinkTables.append(LinkTable[i])

    return LinkTables

topologyLink = topologySave()
app = Flask(__name__)  # type:Flask
app.secret_key="zhang"

#request.path=="/" or request.path=="/login" or request.path=="/zhuce" or request.path=="/" :
@app.before_request
def is_login():
    if request.path!="/index" :
        return None
    if session.get("user1"):
        return None
    else:
        return redirect("/")

@app.route("/")
def login():
    return render_template("log.html")

@app.route("/login",methods=["GET","POST"])
def panduan():
    tag=1
    sftag=None
    sf=request.form.get("peo")
    if sf==None:
        return render_template("log.html",ss="选择用户身份")
    else:
        if sf=='adm':
            userlist = sql.showAlluser()
        else:
            userlist=sql.showAllsuser()
    for i in userlist:
        if request.form.get("user")==i[0] and request.form.get("pwd")==i[1]:
                tag=2
                session["user1"]=i[0]
                break
        else: tag=1
    if tag==2:
        if sf=='adm':
            return redirect("/index")
        else:
            return redirect("/sindex")
    else: return render_template("log.html",ss="用户名密码错误")

@app.route("/index")
def index():
    session["user"]=""
    return render_template("index.html",session_user=session["user1"])

@app.route("/sindex")
def sindex():
    session["user"]=""
    return render_template("sindex.html",session_user=session["user1"])

@app.route("/sinform",methods=["GET","POST"])
def sinform():
    zgh=session["user1"]
    info=sql.sel_sinfo(zgh)
    return render_template("sadm.html",userinfo=info[0])

@app.route("/inform",methods=["GET","POST"])
def inform():
    zgh=session["user1"]
    info=sql.sel_info(zgh)
    return render_template("adm.html",userinfo=info[0])

@app.route("/topology",methods=["GET","POST"])
def topology():
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.USERNAME, 'admin')
    c.setopt(c.PASSWORD, 'admin')
    c.setopt(c.HTTPHEADER, ["Accept:application/xml"])
    c.setopt(c.URL, 'http://127.0.0.1:8181/restconf/operational/network-topology:network-topology')
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    body = buffer.getvalue()
    soup = BeautifulSoup(str(body, encoding="utf-8"))

    for i in range(0,len(topologyLink)):
        topologyLink[i].Dstat='断开'

    HostTable = []
    ip = soup.find_all('ip')
    for i in range(0, len(ip)):
        ss = BeautifulSoup(str(ip[i]))
        host = topologyTable()
        host.DDeviceIP = str(ss.get_text())
        HostTable.append(host)

    mac = soup.find_all('mac')
    for i in range(0, len(mac)):
        ss = BeautifulSoup(str(mac[i]))
        HostTable[i].DDeviceID = "host:"+str(ss.get_text())

    #取出原始的各项数据
    LinkTable = []
    s_tp = soup.find_all('source-tp')
    s_node = soup.find_all('source-node')
    d_tp = soup.find_all('dest-tp')
    d_node = soup.find_all('dest-node')
    for i in range(0, len(s_tp)):
        ss = BeautifulSoup(str(s_tp[i]))
        link = topologyTable()
        link.openflowSPort = str(ss.get_text())
        LinkTable.append(link)
    for i in range(0, len(d_tp)):
        ss = BeautifulSoup(str(d_tp[i]))
        LinkTable[i].openflowDPort = str(ss.get_text())
    for i in range(0, len(s_node)):
        ss = BeautifulSoup(str(s_node[i]))
        LinkTable[i].openflowID = str(ss.get_text())
    for i in range(0, len(d_node)):
        ss = BeautifulSoup(str(d_node[i]))
        LinkTable[i].DDeviceID = str(ss.get_text())

    #去除openflow为host的无效数据
    for l in LinkTable:
        if l.openflowID.find('host') == 0:
            LinkTable.remove(l)
    for l in LinkTable:
        if l.openflowID.find('host') == 0:
            LinkTable.remove(l)
    for l in LinkTable:
        if l.openflowID.find('host') == 0:
            LinkTable.remove(l)
    for l in LinkTable:
        if l.openflowID.find('host') == 0:
            LinkTable.remove(l)

    #为host添加IP
    for l in LinkTable:
        for h in HostTable:
            if h.DDeviceID == l.DDeviceID:
                l.DDeviceIP = h.DDeviceIP

    #修补openflow:1的link不全的bug
    for l in LinkTable:
        if l.DDeviceID == 'openflow:1':
            ll = topologyTable()
            ll.openflowID = l.DDeviceID
            ll.DDeviceID = l.openflowID
            ll.openflowSPort = l.openflowDPort
            ll.openflowDPort = l.openflowSPort
            LinkTable.append(ll)

    #按openflowID对列表排序
    for i in range(0, len(LinkTable)):
        for j in range(0, len(LinkTable)):
            if LinkTable[i].openflowID < LinkTable[j].openflowID:
                LinkTable[i], LinkTable[j] = LinkTable[j], LinkTable[i]

    #openflowID相同，按源端口对列表排序
    for i in range(0, len(LinkTable)):
        for j in range(0, len(LinkTable)):
            if LinkTable[i].openflowSPort < LinkTable[j].openflowSPort:
                if LinkTable[i].openflowID == LinkTable[j].openflowID:
                    LinkTable[i], LinkTable[j] = LinkTable[j], LinkTable[i]

    Links = []
    for l in range(0, len(LinkTable)):
        Links.append(LinkTable[l].openflowID)
        Links.append(LinkTable[l].DDeviceID)

    for i in range(0, len(Links)-1):
        if len(Links) <= i:
            break
        for j in range(i+1, len(Links)):
            if len(Links) <= j:
                break
            if Links[i] == Links[j] and Links[i+1] == Links[j-1] and (j-i) % 2 == 1 and i % 2 == 0:
                del Links[j]
                del Links[j-1]

    # #去除重复的openflowID
    for i in range(1, len(LinkTable)):
        if LinkTable[len(LinkTable)-i].openflowID == LinkTable[len(LinkTable)-i-1].openflowID:
            LinkTable[len(LinkTable)-i].openflowID = ''

    #SPort，DPort修改
    for l in LinkTable:
        ss = l.openflowSPort
        l.openflowSPort = ss[-1]
        if l.openflowDPort.find('openflow') == 0:
            ss = l.openflowDPort
            l.openflowDPort = ss[-1]
        else:
            l.openflowDPort = '1'

    Openflows = []
    for l in LinkTable:
        if l.openflowID != "":
            Openflows.append(l.openflowID)
    Hosts = []
    for l in LinkTable:
        if l.DDeviceIP != "无":
            Hosts.append(l.DDeviceID)


    for i in Openflows:
        for j in range(0,len(topologyLink)):
            if i==topologyLink[j].openflowID:
                topologyLink[j].Dstat="正常"
            else:
                if topologyLink[j].openflowID=='':
                    topologyLink[j].Dstat = topologyLink[j-1].Dstat

    for j in range(0,len(topologyLink)):
        if topologyLink[j].openflowID!='' and topologyLink[j].Dstat=='断开':
            for i in range(0, len(topologyLink)):
                if topologyLink[i].DDeviceID==topologyLink[j].openflowID:
                    topologyLink[i].Dstat='断开'
                    topologyLink[i].Dstat='断开'
    tage=1
    for j in range(0, len(topologyLink)):
        if topologyLink[j].Dstat=='断开':
            tage=2
            break


    # Hosts = Data.dataHost(Hosts)  静态拓扑
    # Links = Data.dataLink(Links)
    # Openflows = Data.dataopenflow(Openflows)
    context = {'HOST': topologyLink,'Hosts': json.dumps(Hosts), 'Openflows': json.dumps(Openflows), 'Links': json.dumps(Links)}
    return render_template('topology.html', context=context,tage=tage)

@app.route("/main")
def ma():
    return render_template("index.html")

@app.route("/updatepwd",methods=["GET","POST"])
def updatepwd():
    user=request.form.get("user")
    pwd=request.form.get("pwd")
    sql.updatepwd(user,pwd)
    return redirect("/inform")

@app.route("/supdatepwd",methods=["GET","POST"])
def supdatepwd():
    user=request.form.get("user")
    pwd=request.form.get("pwd")
    sql.updatepwd(user,pwd)
    return redirect("/useracount")

@app.route("/updateinfo",methods=["GET","POST"])
def updateinfo():
    user=request.form.get("user")
    qq=request.form.get("qq")
    name = request.form.get("name")
    tel = request.form.get("tel")
    email = request.form.get("email")
    home = request.form.get("home")
    sql.updateinfo(user,qq,name,tel,email,home)
    return redirect("/inform")

@app.route("/updatespwd",methods=["GET","POST"])
def updatespwd():
    user=request.form.get("user")
    pwd=request.form.get("pwd")
    sql.updatespwd(user,pwd)
    return redirect("/sinform")

@app.route("/updatesinfo",methods=["GET","POST"])
def updatesinfo():
    user=request.form.get("user")
    qq=request.form.get("qq")
    name = request.form.get("name")
    tel = request.form.get("tel")
    email = request.form.get("email")
    home = request.form.get("home")
    sql.updatesinfo(user,qq,name,tel,email,home)
    return redirect("/sinform")

@app.route("/useracount",methods=["GET","POST"])
def useracount():
    userlist=sql.sel_userlist()
    return render_template("useracount.html",userlist=userlist)

@app.route("/deluser",methods=["GET","POST"])
def deluser():
    use=request.form.get("user")
    sql.deluse(use)
    sql.deluseinfo(use)
    return redirect("/useracount")

@app.route("/selus",methods=["GET","POST"])
def selus():
    use=request.form.get("user")
    date=sql.selu(use)
    return render_template("useracount.html",userlist=date)

@app.route("/insertuser",methods=["GET","POST"])
def insertuser():
    user=request.form.get("user")
    pwd=request.form.get("password")
    sql.insertuse(user,pwd)
    sql.insertuseinfo(user)
    return redirect("/useracount")

@app.route("/zaibei",methods=["GET","POST"])
def zaibei():
    openlist=[]
    for i in topologyLink:
        if i.openflowID!='':
            openlist.append(i.openflowID)
    flowlist = controllerapi.list_flows()
    return render_template("flowManage.html",openlist=openlist,flowlist=flowlist,)

@app.route("/liuliang",methods=["GET","POST"])
def liuliang():
    openflowlist=[]
    for i in topologyLink:
        if i.openflowID!='':
            openflowlist.append(i.openflowID)
    flowList=[]
    flow=[]
    num=[]
    for i in openflowlist:
        if i!='':
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(c.USERNAME, 'admin')
            c.setopt(c.PASSWORD, 'admin')
            c.setopt(c.HTTPHEADER, ["Accept:application/xml"])
            c.setopt(c.URL, "http://127.0.0.1:8181/restconf/operational/opendaylight-inventory:nodes/node/"+i+"/table/0")
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            body = buffer.getvalue()
            soup = BeautifulSoup(str(body, encoding="utf-8"))
            s_tp = soup.find_all('flow')
            j = 0
            for ss in s_tp:
                s_input = ss.find_all("in-port")
                k = BeautifulSoup(str(s_input))
                pk = str(k.get_text())
                if len(pk) > 2:
                    w = ss.find_all("packet-count")
                    ss=BeautifulSoup(str(w[0]))
                    da=str(ss.get_text())
                    flow.append(da)
                    j=j+1
            num.append(j)
    namelist= []
    for i in range(0,len(topologyLink)):
        namelist.append(topologyLink[i].openflowID)
    lengh=len(namelist)
    return render_template("QOSManage.html",flow=flow,namelist=namelist,l=lengh,topologyLink=topologyLink)

#
# @app.route("/liubiaofafang",methods=["GET","POST"])
# def liubiaofafang():
#     s_ip=request.form.get("s_ip")
#     openid=request.form.get("openid")
#     caozuo=request.form.get("cz")
#     in_port=request.form.get("in_port")
#     out_port = request.form.get("out_port")
#     d_ip=request.form.get("d_ip")
#     pro=request.form.get("prov")
#     url="http://127.0.0.1:8181/restconf/operations/sal-flow:add-flow"
#     if caozuo=="forward":
#         file_in = open("forward.json", "r")
#         file_data = json.load(file_in)
#         file_data['input']['match']['in-port'] = in_port
#         file_data['input']['match']['ipv4-source'] = s_ip
#         file_data['input']['match']['ipv4-destination'] = d_ip
#         file_data["input"]["priority"] = pro
#         file_data["input"]["instructions"]["instruction"][0]["apply-actions"]["action"][0]["output-action"][
#             "output-node-connector"] = out_port
#         file_data["input"]["node"] ="/opendaylight-inventory:nodes/opendaylight-inventory:node[opendaylight-inventory:id='"+openid+"']"
#         file=json.dumps(file_data)
#         http_post(url,file)
#         file_in.close()
#
#     else:
#         if caozuo=="drop":
#             file_in = open("drop.json", "r")
#             file_data = json.load(file_in)
#             file_data['input']['match']['in-port'] = in_port
#             file_data['input']['match']['ipv4-source'] = s_ip
#             file_data['input']['match']['ipv4-destination'] = d_ip
#             file_data["input"]["priority"] = pro
#             file_data["input"][
#                 "node"] = "/opendaylight-inventory:nodes/opendaylight-inventory:node[opendaylight-inventory:id='" + openid + "']"
#             file = json.dumps(file_data)
#             http_post(url, file)
#             file_in.close()
#
#     return redirect('/zaibei')

@app.route("/switchinfo",methods=["GET","POST"])
def switchinfo():
    openlist=[]
    for i in topologyLink:
        if i.openflowID!='':
            openlist.append(i)
    return render_template("switchInfo.html",openlist=openlist)

@app.route("/infoset",methods=["GET","POST"])
def infoset():
    for i in topologyLink:
        if i.openflowID!='':
            s= request.form.get(i.openflowID)
            i.Lstat=s

    return redirect("/switchinfo")

@app.route("/deleteflow",methods=["GET","POST"])
def delete_flow():
    swid=request.form.get('swid')
    flowid=request.form.get('id')
    controllerapi.flow_delete(swid,flowid)
    return redirect('/zaibei')

@app.route("/addflow",methods=["POST"])
def add_flow():
    res=dict()
    res["status"]='succes'
    flow_id=request.form.get('flow_id')
    s_ip = request.form.get("s_ip")
    openid = request.form.get("openid")
    caozuo = request.form.get("cz")
    in_port = request.form.get("in_port")
    out_port = request.form.get("out_port")
    x_inport=request.form.get("inport")
    x_outport=request.form.get("outport")
    d_ip = request.form.get("d_ip")
    pro = request.form.get("prov")
    eth_type=request.form.get('ethernet_type')
    layer4=request.form.get('layer4')
    meter=request.form.get('meter')
    post_data={}
    flow_set={
        'id':flow_id,
        'flow-name':flow_id,
        'table_id':0
    }
    if pro:
        flow_set['priority']=pro
    match_set={}
    if in_port:
        match_set['in-port']=in_port
    if eth_type:
        match_set['ethernet-match']={
            "ethernet-type":{
                "type":eth_type
            }
        }
    if s_ip:
        match_set['ipv4-source']=s_ip
    if d_ip:
        match_set['ipv4-destination']=d_ip
    if layer4:
        if "TCP"==layer4:
            match_set['ip-match']={
                "ip-protocol":6
            }
            if in_port:
                match_set['tcp-source-port']=x_inport
            if out_port:
                match_set['tcp-destination-port'] = x_outport
        if "UDP"==layer4:
            match_set['ip-match'] = {
                "ip-protocol": 17
            }
            if in_port:
                match_set['udp-source-port']=x_inport
            if out_port:
                match_set['udp-destination-port'] = x_outport
    flow_set['match']=match_set

    action_set={
        'order':"0"
    }
    action=caozuo
    if action:
        if "DROP" ==action:
            action_set['drop-action']={}
        if "OUTPUT"==action:
            action_set['output-action']={
                "output-node-connector":out_port
            }
    print(meter)
    if meter:
        action_meter = {
            "order": "0",
            "meter": {"meter-id": meter}
        }
        instruc_set = {
            "instruction": [
                action_meter,
                {
                    "order": "1",
                    "apply-actions": {
                        "action": [action_set]
                    }
                }]
        }
    else:
        instruc_set={
            "instruction":[{
                "order":"0",
                "apply-actions":{
                    "action":[action_set]
                }
            }
            ]
        }
    flow_set["instructions"]=instruc_set
    body = json.dumps({"flow":flow_set})
    reply=controllerapi.add_flow(openid,flow_id,body)
    print(reply)
    return redirect('/zaibei')



@app.route("/Qos")
def qosmanage():
    openlist = []
    for i in topologyLink:
        if i.openflowID != '':
            openlist.append(i.openflowID)
    res=controllerapi.list_meter()
    return render_template("/Qos.html",res=res['data'],openlist=openlist)


# @app.route("/add_Qos",methods=["POST"])
# def add_Qos():
#     res=dict()
#     s_port=request.form.get("in_port")
#     d_port=request.form.get("out_port")
#     bursr_size=request.form.get("burst-size")
#     limite=request.form.get("limited-rate")
#     addqos={
#         "input":{
#             "src-port":s_port,
#             "dst-port":d_port,
#             "burst-size":bursr_size,
#             "limited-rate":limite
#         }
#     }
#     body = json.dumps({"qos": addqos})
#     reply=controllerapi.add_qos(body)
#     print(reply)
#     return redirect("/Qos")

@app.route("/add_meter",methods=["POST"])
def addmeter():
    switch_id=request.form.get("swid")
    meter_id=request.form.get("meterid")
    burst_size=request.form.get("burst-size")
    limited=request.form.get("limited-rate")
    rate=request.form.get("rate")
    controllerapi.add_meter(switch_id,meter_id,burst_size,limited,rate)
    return redirect("/Qos")

app.run("0.0.0.0",5000, debug=True)
