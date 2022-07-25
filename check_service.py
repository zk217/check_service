#!/usr/bin/python
#coding=utf-8

import socket
import sys
import traceback
import paramiko
import urllib
import MySQLdb
import MySQLdb.cursors

def telnet(ip,port,timeout = 1):
    socketobj = None
    success = False
    try :
        socketobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketobj.settimeout(timeout)
        socketobj.connect((ip,int(port)))
        success = True
    except :
        print 'Exception has occured : ' + traceback.format_exc()
    finally :
        if socketobj != None :
            socketobj.close()
        return success

def connect(ip,user,password,port = 22):
    client = None
    connected = False
    try :
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try :
            client.connect(ip,port,user,password)
        except:
            client.connect(ip,port,user,password,look_for_keys=False)
        connected = True
    except :
        print 'Exception has occured : ' + traceback.format_exc()
    finally :
        if client != None and connected:
            client.close()
        return connected

def mysql(host,port,user,passwd,db):
    conn = None
    try:
         conn = MySQLdb.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset="utf8",cursorclass = MySQLdb.cursors.DictCursor)
    except :
        print 'Exception has occured : ' + traceback.format_exc()
    finally :
        if conn != None :
            conn.close()
        return conn != None

# ======check ssh======
SERVICE_SSH_IP = '112.51.0.155'
SERVICE_SSH_PORT = 22
SERVICE_SSH_USER = 'root'
SERVICE_SSH_PASSWD = 'qazwsx11'

print 'Checking SSH...'
success = telnet(SERVICE_SSH_IP,SERVICE_SSH_PORT)
if success:
    print 'SSH service is OK'
    success = connect(SERVICE_SSH_IP,SERVICE_SSH_USER,SERVICE_SSH_PASSWD,SERVICE_SSH_PORT)
    print 'SSH authentication is OK' if success else 'SSH authentication is failed'
else:
    print 'SSH service is dead'

# ======check web======
SERVICE_WEB_IP = '112.51.0.155'
SERVICE_WEB_PORT = 80
SERVICE_WEB_APP = 'http://112.51.0.155/static/dUCEN4ry/client/client.zip'

print 'Checking WEB...'
success = telnet(SERVICE_WEB_IP,SERVICE_WEB_PORT)
if success:
    print 'WEB service is OK'
    try:
        urllib.urlretrieve(SERVICE_WEB_APP, "client.zip")
        print 'WEB request is OK'
    except:
        print 'WEB request is failed'
else:
    print 'WEB service is dead'

# ======check mysql======
SERVICE_MYSQL_IP = '112.51.0.155'
SERVICE_MYSQL_PORT = 3307
SERVICE_MYSQL_USER = 'root'
SERVICE_MYSQL_PASSWD1 = 'pJnG3ji7'
SERVICE_MYSQL_PASSWD2 = 'gwwyT9fM'
SERVICE_MYSQL_DB = 'web'

print 'Checking MySQL...'
success = telnet(SERVICE_MYSQL_IP,SERVICE_MYSQL_PORT)
if success:
    print 'MySQL service is OK'
    if mysql(SERVICE_MYSQL_IP,SERVICE_MYSQL_PORT,SERVICE_MYSQL_USER,SERVICE_MYSQL_PASSWD1,SERVICE_MYSQL_DB):
        print 'MySQL first authentication is OK'
    elif mysql(SERVICE_MYSQL_IP,SERVICE_MYSQL_PORT,SERVICE_MYSQL_USER,SERVICE_MYSQL_PASSWD2,SERVICE_MYSQL_DB):
        print 'MySQL second authentication is OK'
    else:
        print 'MySQL authentication is failed'
else:
    print 'MySQL service is dead'

# ======check rdp======
SERVICE_RDP_IP = '112.51.0.155'
SERVICE_RDP_PORT = 3389
SERVICE_RDP_USER = 'administrator'
SERVICE_RDP_PASSWD = 'power123'

print 'Checking RDP...'
success = telnet(SERVICE_RDP_IP,SERVICE_RDP_PORT)
if success:
    print 'RDP service is OK'
    # rdp authentication unsupported now
else:
    print 'RDP service is dead'

print 'ALL DONE'
