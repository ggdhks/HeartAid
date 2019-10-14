#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lsqlite import db
from lsqlite.orm import Model, StringField, BooleanField, FloatField, TextField,IntegerField
import config
import time


def raw_choose(message):
    choose = raw_input(message + ' [y/n]')
    return choose.strip().lower() in ['y', 'yes']

def trans_time(data):
    if len(str(data))>=2:
        return str(data)
    else:
        return "0"+str(data)


class UserTable(Model):
    __table__ = 'UserTable'

    ID = IntegerField(primary_key=True, updatable=False, ddl='int(6)')
    Password = StringField(ddl='varchar(15)')
    Nickname = StringField(ddl='varchar(15)')
    Email = StringField(ddl='varchar(25)')
    Lastdate = StringField(ddl='varchar(10)',default = "1995-04-15")
    Lasttime = StringField(ddl='varchar(8)',default = "23-60-60") 


def insert_UserTable(id,password,nickname,email):
    Date = trans_time(time.localtime().tm_year) +"_"+trans_time(time.localtime().tm_mon)+"_"+trans_time(time.localtime().tm_mday)
    Time = trans_time(time.localtime().tm_hour) +"_"+trans_time(time.localtime().tm_min)+"_"+trans_time(time.localtime().tm_sec)
    UserTable(ID = id,Password = password,Nickname = nickname, Email = email, Lastdate = Date , Lasttime = Time).insert();


def update_UserTable_time(id):
    Date = trans_time(time.localtime().tm_year) +"_"+trans_time(time.localtime().tm_mon)+"_"+trans_time(time.localtime().tm_mday)
    Time = trans_time(time.localtime().tm_hour) +"_"+trans_time(time.localtime().tm_min)+"_"+trans_time(time.localtime().tm_sec)
    db.update('update UserTable set Lastdate=?, Lasttime=? where ID=?', Date, Time, id)

def select_UserTable_time(id):
    return db.select("select Lastdate from UserTable where ID = ?" , id)[0]["Lastdate"],db.select("select Lasttime from UserTable where ID = ?" , id)[0]["Lasttime"]


def Friend_Table(id):
    class FriendTable(Model):
        __table__ = 'F'+str(id)
        ID= IntegerField(primary_key=True,updatable=False,ddl='int(20)')
        Nickname = StringField(ddl='varchar(15)')
        Status = StringField(ddl='varchar(1)')
        LID = IntegerField(ddl='int(5)')
    return FriendTable

def Check_Friend_Table(id):
    return db.select("select count(*) from sqlite_master where type='table' and name = ?","F"+str(id))[0]["count(*)"] 



def create_FriendTable(id):
    FriendTable = Friend_Table(id)
    db.update('drop table if exists %s' %  FriendTable.__table__ )
    db.update(FriendTable().__sql__())


def insert_FriendTable(id,FID):
    nickname = find_nickname(FID)
    FriendTable = Friend_Table(id)(ID = FID,Nickname = nickname,Status = "F",LID = 1)
    FriendTable.insert()

def delete_FriendTable(id,FID):
    db.update("delete from "+"F"+str(id)+" where ID = ?",FID)

def change_List(id,fid,listname):
    lid = db.select("select LID from "+"L"+str(id)+" where Listname =?",listname)[0]["LID"]
    print("lid",lid)
    db.update("update "+ 'F'+str(id)+" set LID = "+str(lid) + " where ID=?",fid )

def List_Table(id):
    class ListTable(Model):
        __table__ = 'L'+str(id)
        LID = IntegerField(primary_key=True,updatable = False,ddl='int(5)',default = 1)
        Listname = StringField(ddl = 'varchar(10)',default = u"我的好友")
    return ListTable

def create_ListTable(id):
    ListTable = List_Table(id)
    db.update('drop table if exists %s' %  ListTable.__table__ )
    db.update(ListTable().__sql__())
    ListTable(LID = 1,Listname = u"我的好友").insert()

def MAX_LID(id):
    return db.select_int("select count(*) from "+'L'+str(id))

def insert_ListTable(id,listname):
    lid = MAX_LID(id) + 1
    ListTable = List_Table(id)(LID = lid,Listname = listname)
    ListTable.insert()

def delete_ListTable(id,LID):
    db.update("delete from "+"L"+str(id)+" where LID = ?",LID)

def select_ListTable(id):
    return db.select("select * from "+"L"+str(id))

def Chat_Table(id):
    class ChatTable(Model):
        __table__ = 'C'+str(id)
        CID = IntegerField(primary_key=True,updatable = False,ddl='int(5)')
        Senderid = IntegerField(ddl='int(10)')
        Receiverid = IntegerField(ddl='int(10)')
        Message = StringField(ddl = 'varchar(1000)')
        Date = StringField(ddl='varchar(10)')
        Time = StringField(ddl='varchar(10)')
    return ChatTable

def create_ChatTable(id):
    ChatTable = Chat_Table(id)
    db.update('drop table if exists %s' %  ChatTable.__table__ )
    db.update(ChatTable().__sql__())

def MAX_CID(id):
    return db.select_int("select count(*) from "+'C'+str(id))

def insert_ChatTable(id,senderid,receiverid,message):
    DATE = trans_time(time.localtime().tm_year) +"_"+trans_time(time.localtime().tm_mon)+"_"+trans_time(time.localtime().tm_mday)
    TIME = trans_time(time.localtime().tm_hour) +"_"+trans_time(time.localtime().tm_min)+"_"+trans_time(time.localtime().tm_sec)
    cid = MAX_CID(id)+1
    ChatTable = Chat_Table(id)(CID = cid,Senderid = senderid,Receiverid = receiverid,Message = message,Date = DATE,Time = TIME)
    ChatTable.insert()

def select_ChatTable(id):
    return db.select("select * from "+"C"+str(id))

class GroupTable(Model):
    __table__ = 'GroupTable'
    GID = IntegerField(primary_key=True,updatable = False, ddl='int(10)')
    Groupname = StringField(ddl = 'varchar(20)')


def insert_GroupTable(gid,groupname):
    GroupTable(GID = gid,Groupname = groupname).insert();

def delete_GroupTable(gid):
    db.update("delete from GroupTable where GID = ?",gid)

def create_group(id,gid,groupname):
    insert_GroupTable(gid,groupname)
    create_GPTable(gid)
    insert_GPTable(gid,id)
    insert_PGTable(id,gid)

def add_group(id,gid):
    insert_GPTable(gid,id)
    insert_PGTable(id,gid)

def Group_has_people_Table(gid):
    class GPTable(Model):
        __table__ = 'GP'+str(gid)
        ID = IntegerField(primary_key=True,updatable = False,ddl='int(5)',default = 1)
    return GPTable

def create_GPTable(gid):
    GPTable = Group_has_people_Table(gid)
    db.update(GPTable().__sql__())

def insert_GPTable(gid,uid):
    GPTable = Group_has_people_Table(gid)(ID = uid)
    GPTable.insert()

def delete_GPTable(gid,uid):
    db.update("delete from "+"GP"+str(gid)+" where ID = ?",uid)

def select_people_in_group(gid):
    return db.select("select ID from GP"+str(gid))

def People_has_groups_Table(uid):
    class PGTable(Model):
        __table__ = 'PG'+str(uid)
        GID = IntegerField(primary_key=True,updatable = False,ddl='int(5)')
    return PGTable

def create_PGTable(uid):
    PGTable = People_has_groups_Table(uid)
    db.update('drop table if exists %s' %  PGTable.__table__ )
    db.update(PGTable().__sql__())

def insert_PGTable(uid,gid):
    PGTable = People_has_groups_Table(uid)(GID = gid)
    PGTable.insert()

def delete_PGTable(uid,gid):
    db.update("delete from "+"PG"+str(uid)+" where GID = ?",gid)

def select_gid(id):
    return db.select("select GID from "+"PG"+str(id))

def get_groups(id):
    gid = select_gid(id)
    print("gid",gid)
    output = []
    for i in gid:
        a = db.select("select * from GroupTable where GID = ?",str(i["GID"]))
        output.append(a[0])
    return output

def check_email(email):
    if (email.find('@')>1 and email.find('.')>4 and email.find('.')>email.find('@') and email.find('.')<len(email)-3):
        return True
    else:
        return False

def new_user(id,password,nickname,email):
    if (check_email(email)):
        insert_UserTable(id,password,nickname,email)
        create_ChatTable(id)
        create_PGTable(id)
        create_ListTable(id)
        create_FriendTable(id)
        return True
    else:
        return False

def check_login(id,password): 
    return len(db.select("select * from UserTable where ID = ? and password = ?", id,password))

def get_friends(id):
    a = db.select("select * from %s" % 'F'+str(id))
    id_list = []
    nickname_list = []
    status_list = []
    lid_list = []
    for i in a:
        id_list.append(i["ID"])
        nickname_list.append(i["Nickname"])
        status_list.append(i["Status"])
        lid_list.append(i["LID"])
    return id_list,nickname_list,status_list,lid_list

def find_nickname(id):
    return db.select("select Nickname from UserTable where ID = ? ", id)[0]["Nickname"]

def apply_FriendTable(id,FID):
    nickname = find_nickname(id)
    FriendTable = Friend_Table(FID)(ID = id,Nickname = nickname,Status = "A",LID = 1)
    FriendTable.insert()

def pass_FriendTable(applyid,passid):
    nickname = find_nickname(passid)
    FriendTable = Friend_Table(applyid)(ID = passid,Nickname = nickname,Status = "F",LID = 1)
    FriendTable.insert()
    db.update("update "+ 'F'+str(passid)+" set Status='F' where ID=?",applyid )

def refuse_FriendTable(applyid,passid):
    delete_FriendTable(passid,applyid)

def add_friend(id,aid):
    if len(db.select("select * from UserTable where ID = ?", aid)) == 0:
        return 0
    if  len(db.select("select * from "+"F"+str(id)+" where ID = ?", aid)) == 1:
        return 2
    if id == aid:
        return 3
    apply_FriendTable(id,aid)
    return 1

def compare_time(date1,time1,date2,time2):
    if date1<date2 :
        return 0
    if date1>date2:
        return 1
    if date1==date2:
        if time1<time2:
            return 0
        if time1>time2:
            return 1
        return 0


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if raw_choose('Initialize all the table in %s?' % config.database):
        L = []
        L.append(UserTable)
        # L.append(GroupTable)
        db.create_engine(config.database);
        for m in L:
            db.update('drop table if exists %s' % m.__table__)
            db.update(m().__sql__())

    a = new_user(10000,"123456", "Gessii","2573955647@qq.com")  #中文字符加u
    b = new_user(10001,"123456", "Ggd", "2573955647@qq.com")
    c = new_user(10002,"123456", "Johnny", "2573955647@qq.com")
    d = new_user(10003,"123456", "Alicia", "2573955647@qq.com")
    d = new_user(10004,"123456", "Emma", "2573955647@qq.com")


