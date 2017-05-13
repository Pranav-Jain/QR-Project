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

def check_update():
        slave_file = find_slave_file()                
        print(slave_file)
	file = [{'input': slave_file}]
	print("checking for update...")
	s = json.dumps(file)
	try:
		res = requests.post("http://192.168.1.102:5000/check/", json=s).json()
		check = res['check']
		rec_file_name = res['file_name']
		print (check)
		print (rec_file_name)
		
		if(res['url']==''):
			print ('Update Not Found')
		else:
			print (res['url'])
			try:
				urllib.urlretrieve(res['url'],rec_file_name)
				print ("file retrieved")
				sp.call("pkill python3",shell=True)
				print("proc killed")
				os.remove(slave_file)
				print("file removed")				
				print("update completed")
				run_slave(rec_file_name)
			except:
				print("inner except")
	except:
		print("error contacting server")
	threading.Timer(2, check_update).start()

def run_slave(slave_file):
        cmd = "python3 " + slave_file
        sp.Popen(cmd, shell=True)


def find_slave_file():
        for file in os.listdir('.'):
                if fnmatch.fnmatch(file, 'slave*.py'):
                        return str(file)

try:
        run_slave(find_slave_file())
        print("slave file started running")
        
except:
        print("error running slave file")
check_update()                        
