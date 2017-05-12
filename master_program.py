#!/usr/bin/env python

import subprocess as sp
import urllib
import threading
import sys
import json
import requests
import urllib
import glob
import os
import shutil
print("Hello")
global slave_file
slave_file = "slave.py"
def check_update():
	file = [{'input': slave_file}]
	print("Update checking")
	s = json.dumps(file)
	#global slave_file = "lcdqr.py"
	try:
		res = requests.post("http://192.168.1.111:5000/check/", json=s).json()
		check = res['check']
		rec_file_name_dir=os.path.join(os.getcwd,res['file_name'])
		print (check)
		print (rec_file_name)
		if(res['url']==''):
			print ('File Not Found')
		else:
			print (res['url'])
			try:
				urllib.urlretrieve(res['url'],os.path.join(update_directory,rec_file_name))
				print ("file retrieved")
				command = 'ps aux | grep name | grep -v grep | awk "{print $2}"'
				process = sp.call(command, shell = True)
				sp.call('pkill -9 '+process, shell=True)
				delete_cmd = "rm "+slave_file
				sp.call(delete_cmd , shell=True)
				shutil.move(os.path.join(update_directory,rec_file_name),os.getcwd())
				os.rename(rec_file_name,slave_file)
				os.execv(sys.executable, ['python'] + sys.argv)
				print("update completed")
			except:
				print("inner except")
		#os.remove(slave_file)
	except:
		print("outer except")
	threading.Timer(2, check_update).start()

update_directory = os.path.join(os.getcwd(),"update")
if not os.path.exists(update_directory):
    os.makedirs(update_directory)

check_update()
#cmd = "python3 " + slave_file
#sp.Popen(cmd, shell=True)
