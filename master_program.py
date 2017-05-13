#!/usr/bin/env python

import subprocess as sp
import urllib
import threading
import sys
import json
import requests
import urllib
import os
import fnmatch
import time
import datetime
from uuid import getnode as get_mac

def check_update():
	slave_file = find_slave_file()                
	file = [{'input': slave_file,'mac':str(get_mac())}]
	make_log("checking for update")
	s = json.dumps(file)
	try:
		res = requests.post("http://192.168.1.102:5000/check/", json=s).json()
                make_log("request made to server")
		check = res['check']
                make_log ("return status: "+str(check))
		rec_file_name = res['file_name']
		make_log ("file with server: "+rec_file_name)
		make_log ("file with client(RPi): "+slave_file)
		if(res['url']==''):
			make_log ('Update Not Found')
		else:
			make_log (res['url'])
			try:
				urllib.urlretrieve(res['url'],rec_file_name)
				make_log ("file retrieved")
				sp.call("pkill python3",shell=True)
				make_log ("slave process killed")
				os.remove(slave_file)
				make_log ("previous slave file removed")				
				make_log ("update completed")
				run_slave(rec_file_name)
				make_log ("updated slave file called to run")
			except:
				make_log ("inner except")
	except:
		make_log ("error contacting server")
	threading.Timer(10, check_update).start()

def run_slave(slave_file):
        cmd = "python3 " + slave_file
        sp.Popen(cmd, shell=True)
        make_log ("slave started running")


def find_slave_file():
        for file in os.listdir('.'):
                if fnmatch.fnmatch(file, 'slave*.py'):
                        return str(file)

def make_log(string):
	try:
		f=open("Master_Log.txt", "a+")
	except IOError:
		f = open("Master_log.txt", "w")
	ts= time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	data_raw= "["+st+"]  "+string+'\n'
	print(data_raw)
	f.write(data_raw)
	f.flush()

make_log("master started")
try:
        run_slave(find_slave_file())
        
except:
        make_log ("error running slave file")

check_update()                        
