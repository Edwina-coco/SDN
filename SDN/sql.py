import pymysql

# Simple DB access layer (MySQL):
# Handles user auth records and profile records.

db=pymysql.connect("localhost","zgh","123456","test")
cusor=db.cursor();
# cusor.execute("select answer from answer_que")
# data = cusor.fetchall()
# print(data[1])
def showAlluser():
    # Query all admin login accounts.
    cusor.execute("select * from user")
    data = cusor.fetchall()
    if data == None:
        return None
    else:
        return data
def showAllsuser():
    # Query all standard login accounts.
    cusor.execute("select * from suser")
    data = cusor.fetchall()
    if data == None:
        return None
    else:
        return data


def sel_info(str):
    # Query admin profile by username.
    cusor.execute("SELECT * from infom WHERE user='"+str+"'")
    data = cusor.fetchall()
    if data==None:
        return None
    else:return data

def sel_sinfo(str):
    # Query standard user profile by username.
    cusor.execute("SELECT * from sinfom WHERE user='"+str+"'")
    data = cusor.fetchall()
    if data==None:
        return None
    else:return data

def updatepwd(user,pwd):
    # Update admin password.
    cusor.execute("update user set password='"+pwd+"' where user='"+user+"'")
    db.commit()

def updateinfo(user,qq,name,tel,email,home):
    # Update admin profile fields.
    cusor.execute("update infom set name='" + name + "',tel='"+tel+"',email='"+email+"',qq='"+qq+"',home='"+home+"'  where user='" + user + "'")
    db.commit()

def updatespwd(user,pwd):
    # Update standard user password.
    cusor.execute("update suser set pwd='"+pwd+"' where user='"+user+"'")
    db.commit()

def updatesinfo(user,qq,name,tel,email,home):
    # Update standard user profile fields.
    cusor.execute("update sinfom set name='" + name + "',tel='"+tel+"',email='"+email+"',qq='"+qq+"',home='"+home+"'  where user='" + user + "'")
    db.commit()

def sel_userlist():
    # Query full profile list for management page.
    cusor.execute("SELECT * from infom")
    data = cusor.fetchall()
    if data == None:
        return None
    else:
        return data

def deluse(str):
    # Delete admin login record.
    cusor.execute("delete from user where user='"+str+"'")
    db.commit()

def deluseinfo(str):
    # Delete admin profile record.
    cusor.execute("delete from infom where user='"+str+"'")
    db.commit()

def selu(str):
    # Query one user profile by username (for search).
    cusor.execute("SELECT * from infom WHERE user='"+str+"'")
    data = cusor.fetchall()
    if data==None:
        return None
    else:return data

def insertuse(user,pwd):
    # Insert admin login record.
    cusor.execute("insert into user (user,password) values ('"+user+"','"+pwd+"')")
    db.commit()
def insertuseinfo(user):
    # Initialize empty admin profile record.
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
