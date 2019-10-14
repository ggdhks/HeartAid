#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.websocket
import handler
from handler import BaseHandler
import config
import models
import random
from lsqlite import db
class SocketHandler(tornado.websocket.WebSocketHandler):
	clients = dict()

	def open(self):
		id = self.get_secure_cookie(config._id)
		print "open id:",id
		SocketHandler.clients[id] = self
		print "on",SocketHandler.clients

	def on_close(self):
		id = self.get_secure_cookie(config._id)
		print "close id:",id
		del SocketHandler.clients[id]
		models.update_UserTable_time(id)

	def send_friend_message(self,id,message):
		if (SocketHandler.clients.has_key(id)==True):
			friend = SocketHandler.clients[id]
			friend.write_message(message)

	def send_apply_message(self,result,applyid,passid):
		if (SocketHandler.clients.has_key(applyid)==True):	
			user = SocketHandler.clients[applyid]
			if result == "P":
				pass
			if result == "R":
				pass

	def send_group_message(self,id,gid,message):
		fid = models.select_people_in_group(gid)
		user = []
		for i in fid:
			if str(i["ID"])== str(id):
				continue
			user.append(i["ID"])
		if len(user)==0:
			return
		for i in user:
			if SocketHandler.clients.has_key(str(i))==True:
				friend = SocketHandler.clients[str(i)]
				friend.write_message(message)
				print "message",message
			else:
				continue


	def on_message(self,data):

		id = self.get_secure_cookie(config._id)
		nickname = models.find_nickname(id)
		print "message id ",id
		print "on_message data:",data

		if data[0]=="C":
			interrupt = data.index('_')
			fid = data[1:interrupt]
			fmessage = data[interrupt+1:]
			self.send_friend_message(fid,"C"+id+"_"+nickname+"@"+fmessage)
			models.insert_ChatTable(id,id,fid,fmessage)
			models.insert_ChatTable(fid,id,fid,fmessage)

		if data[0]=="A":
			fid = data[1:]
			a = models.add_friend(id,fid)
			self.write_message(str(a))

		if data[0]=="P" or data[0]=="R":
			interrupt = data.index('_')
			applyid = data[1:interrupt]
			passid = data[interrupt+1:]
			models.pass_FriendTable(applyid,passid)
			self.write_message(data[0]+"_"+applyid)
			self.send_apply_message(data[0],applyid,passid)

		if data[0]=="L" and data[1]=="A":
			interrupt = data.index('_')
			new_list_name = data[interrupt+1:]
			models.insert_ListTable(id,new_list_name)
		if data[0]=="L" and data[1]=="C":
			interrupt1 = data.index('_')
			interrupt2 = data.index('@')
			fid = data[interrupt1+1:interrupt2]
			listname = data[interrupt2+1:]
			print fid,listname
			models.change_List(id,fid,listname)
		if data[0]=="G" and data[1]=="C":
			interrupt = data.index('_')
			groupname = data[interrupt+1:]
			print groupname

			a = [0]
			while (len(a)!=0):
				gid = random.randint(1000000,9999999)
				a = db.select("select * from GroupTable where GID = ?",gid)
			print "gid",gid
			models.create_group(id,gid,groupname)

		if data[0]=="G" and data[1]=="A":
			interrupt = data.index('_')
			groupid = data[interrupt+1:]
			print groupid
			models.add_group(id,groupid)

		if data[0]=="G" and data[1]=="G":
			interrupt = data.index('_')
			groupid = data[2:interrupt]
			message = data[interrupt+1:]
			print "groupid,message",groupid,message
			self.send_group_message(id,groupid,"G"+groupid+"_"+nickname+"@"+message)



