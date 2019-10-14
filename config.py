#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, os
from tornado.options import define, options

define("config",
    type=str,
    callback=lambda path: options.parse_config_file(path, final=False),
    help="path to config file")

define('webport',
    default=8080, type=int,
    help='port at running web server at')
define('socketport',
    default=8081, type=int,
    help='port that running socket server at')

define('filesize',
    default=1024 * 1024, type=int,
    help='the maximun file size of user can upload')
define('cookie_secret',
    default="XmuwPAt8wHdnik4Xvc3GXmbXLifVmPZYhoc9Tx4x1iZ", type=str,
    help='the secret cookie')
define('database',
    default='user.db', type=str,
    help='the sqlite database file')
define('messageInterval',
    default=2, type=int,
    help='the minimum interval between two message')

define('unauthsize',
    default=32, type=int,
    help='the connection number without authorization kept by server')
define('separator',
    default='\n', type=str,
    help='the separator that seperate the message in socket')

define('rtmpHost',
    default='localhost', type=str,
    help='the RTMP server for push video flow')
define('rtmpPushPort',
    default=6666, type=int,
    help='the RTMP server port for push video flow')
define('rtmpPullPort',
    default=1935, type=int,
    help='the RTMP server port for PULL flow')
define('rtmpAppName',
    default='live', type=str,
    help='the RTMP server Application name for pull flow')

define('userCountSend',
    default=False, type=bool,
    help='send user number to central server')
define('sendPeriod',
    default=5000, type=int,
    help='the interval of sending')
define('sendHost',
    default='localhost', type=str,
    help='the host of central server')
define('sendPort',
    default=8080, type=int,
    help='the port of central server')
define('sendURL',
    default='/api/report', type=str,
    help='the url that accept user infomation')
define('device_id',
    default=10000, type=int,
    help='the device_id of this server')
define('auth_key',
    default='None', type=str,
    help='the authenticated key of this server')
define('_id',
    default='id', type=str,
    help='cookie name of id')
define('_identity',
    default='identity', type=str,
    help='cookie name of identity')
define('_password',
    default='password', type=str,
    help='cookie name of password')
define('_nickname',
    default='nickname', type=str,
    help='cookie name of nickname')
define('_email',
    default='email', type=str,
    help='cookie name of email')
define('_age',
    default='age', type=int,
    help='cookie name of age')

version = "0.4.1"

class Type:
    action = 0
    status = 1
    operation = 2
    info = 3

class Action:
    acquire = "acquire"
    release = "release"
    authorize = "authorize"
    broadcast = "broadcast"

class Status:
    authorized = "authorized"
    auth_failed = "auth_failed"
    file_upload = "file_uploaded"

class Info:
    user_changed = "user_changed"
    fpga_disconnected = "fpga_disconnected"
    broadcast = "broadcast"

settings = dict(
    cookie_secret = options.cookie_secret,
    template_path = os.path.join(os.path.dirname(__file__), "templates"),  #
    static_path = os.path.join(os.path.dirname(__file__), "static"),       #
    static_url_prefix = "/static/",
    login_url = '/login',
    xsrf_cookies = False,
    debug = True,
)

options.parse_command_line()

def checkSeparator():
    global separatorLen
    separatorLen = len(options.separator)
    if separatorLen <= 0:
        raise ValueError("separator '%s' is invalid" % options.separator)
testList = []
testList.append(checkSeparator)
for func in testList:
    func()

globals().update(options.as_dict())

def show():
    print("options = ", json.dumps(options.as_dict(), indent = 4))
    print("settings = ", json.dumps(settings, indent = 4))
    print("version = %s" % version)

if __name__ == '__main__':
	show()
