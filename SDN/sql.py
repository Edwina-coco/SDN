import pymysql
db=pymysql.connect("localhost","zgh","123456","test")
cusor=db.cursor();
# cusor.execute("select answer from answer_que")
# data = cusor.fetchall()
# print(data[1])
def showAlluser():
    cusor.execute("select * from user")
    data = cusor.fetchall()
    if data == None:
        return None
    else:
        return data
def showAllsuser():
    cusor.execute("select * from suser")
    data = cusor.fetchall()
    if data == None:
        return None
    else:
        return data


def sel_info(str):
    cusor.execute("SELECT * from infom WHERE user='"+str+"'")
    data = cusor.fetchall()
    if data==None:
        return None
    else:return data

def sel_sinfo(str):
    cusor.execute("SELECT * from sinfom WHERE user='"+str+"'")
    data = cusor.fetchall()
    if data==None:
        return None
    else:return data

def updatepwd(user,pwd):
    cusor.execute("update user set password='"+pwd+"' where user='"+user+"'")
    db.commit()

def updateinfo(user,qq,name,tel,email,home):
    cusor.execute("update infom set name='" + name + "',tel='"+tel+"',email='"+email+"',qq='"+qq+"',home='"+home+"'  where user='" + user + "'")
    db.commit()

def updatespwd(user,pwd):
    cusor.execute("update suser set pwd='"+pwd+"' where user='"+user+"'")
    db.commit()

def updatesinfo(user,qq,name,tel,email,home):
    cusor.execute("update sinfom set name='" + name + "',tel='"+tel+"',email='"+email+"',qq='"+qq+"',home='"+home+"'  where user='" + user + "'")
    db.commit()

def sel_userlist():
    cusor.execute("SELECT * from infom")
    data = cusor.fetchall()
    if data == None:
        return None
    else:
        return data

def deluse(str):
    cusor.execute("delete from user where user='"+str+"'")
    db.commit()

def deluseinfo(str):
    cusor.execute("delete from infom where user='"+str+"'")
    db.commit()

def selu(str):
    cusor.execute("SELECT * from infom WHERE user='"+str+"'")
    data = cusor.fetchall()
    if data==None:
        return None
    else:return data

def insertuse(user,pwd):
    cusor.execute("insert into user (user,password) values ('"+user+"','"+pwd+"')")
    db.commit()
def insertuseinfo(user):
    cusor.execute("insert into infom (user) values ('"+user+"')")
    db.commit()

# def saveOpenflow(str):
#     cusor.execute("insert into openflow (id) values ('" + str + "')")
#     db.commit()
#
# def selopen():
#     cusor.execute("SELECT * from openflow")
#     data = cusor.fetchall()
#     if data == None:
#         return None
#     else:
#         return data