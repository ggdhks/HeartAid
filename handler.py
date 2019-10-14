#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import config
import models
from lsqlite import db
import random
import os.path
from models import new_user,check_login,find_nickname
from rf import is_target

class BaseHandler(tornado.web.RequestHandler):
    def get_current_id(self):
        a = self.get_secure_cookie(config._id)
        return a
    def set_current_id(self, id):
        self.set_secure_cookie(config._id, id)

    def get_current_nickname(self):
        a = self.get_secure_cookie(config._nickname)
        return a
    def set_current_nickname(self, nickname):
        self.set_secure_cookie(config._nickname, nickname)

class DataHandler(BaseHandler):
    def get(self):
        self.render("data.html")

class HeartHandler(BaseHandler):
    def get(self):
        self.render("heart.html")

class MainHandler(BaseHandler):
    def get(self):
        self.render("main.html")

class ModelHandler(BaseHandler):
    def get(self):
        self.render("model.html")

class PasswordHandler(BaseHandler):
    def get(self):
        self.render("password.html")

class PredictHandler(BaseHandler):
    def get(self):
        self.render("predict.html")
    
class ResultHandler(BaseHandler):
    def post(self):
        nickname = self.get_current_nickname()
        age = self.get_argument("r_age")
        sex = self.get_argument("r_sex")
        chest = self.get_argument("r_chest")
        rest = self.get_argument("r_rest")
        serum = self.get_argument("r_serum")
        fast = self.get_argument("r_fast")
        resting = self.get_argument("r_resting")
        maxi = self.get_argument("r_maxi")
        exercise = self.get_argument("r_exercise")
        old = self.get_argument("r_old")
        slope = self.get_argument("r_slope")
        ca = self.get_argument("r_ca")
        thal = self.get_argument("r_thal")

        flag = is_target(age, sex, chest, rest, serum, fast, resting, maxi, exercise, old, slope, ca, thal)
        #flag = 0
        if flag == 1 :
            risk="You may have a risk of heart disease."
            advice="For your health, please make an appointment with your doctor for further treatment. "
            # feature = " woauhgdls"
        elif flag == 0:
            risk="Congratulations, according to our algorithm, you are not at risk of heart disease."
            advice="Although there is no risk of heart disease, you should always go to the hospital to check your body."
            # feature = "None"
        else:
            risk="Error"
            advice="Please predict again."
            # feature = "None"
        
        self.render(
            "result.html",
            nickname_r=nickname, 
            age_r=age,
            sex_r=sex,
            chest_r=chest,
            rest_r=rest,
            serum_r=serum,
            fast_r = fast,
            resting_r = resting,
            maxi_r = maxi,
            exercise_r = exercise,
            old_r = old,
            slope_r = slope,
            ca_r = ca,
            thal_r = thal,
            risk_r = risk,
            advice_r = advice
        )

class LoginCookieHandler(BaseHandler):
    def login(self,id,password):
        a = check_login(id,password)
        if a==1:
            self.set_current_id(id) 
            self.redirect("/main",permanent = True)
        elif a==0:
            self.write("<html><body><script type=\"text/JavaScript\">alert(\"wrong user name or password\"); window.history.back()</script></html>")
        else:
            self.write("<html><body><script type=\"text/JavaScript\">alert(\"system error\"); window.history.back()</script></html>")

    def logout(self):
        self.clear_cookie(config._id)
    def post(self):
        self.logout()
        self.redirect("/login",permanent = True)

class LoginHandler(LoginCookieHandler):
    def get(self):
        self.render("login.html")
    def post(self):
        id = self.get_argument(config._id)
        password = self.get_argument(config._password)
        self.login(id,password)

class LogoutHandler(BaseHandler):
    def get(self):
        if (self.get_argument("logout", None)):
            self.clear_cookie(config._id)
            self.redirect("/login")

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html")
    def post(self):
        nickname = self.get_argument("nickname")
        password1 = self.get_argument("password1")
        password2 = self.get_argument("password2")
        email = self.get_argument("email")
        
        self.set_current_nickname(nickname)

        if (password1!=password2):
            self.write("<html><body><script type=\"text/JavaScript\">alert(\"passwords are different\"); window.history.back()</script></html>")
 
        a = [0]
        while (len(a)!=0):
            id = random.randint(100000,999999)
            a = db.select("select * from UserTable where ID = ?",id)

        if (new_user(id,password1,nickname,email)): 
            self.render("rsuccess.html",id = id, rr_nickname = nickname) 
        else:
            self.write("<html><body><script type=\"text/JavaScript\">alert(\"E-mail format is incorrect\"); window.history.back()</script></html>")

