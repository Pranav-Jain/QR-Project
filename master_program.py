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
import fnmatch

global slave_file


def check_update():
        print(slave_file)
	file = [{'input': slave_file}]
	print("Update checking")
	s = json.dumps(file)
	#global slave_file = "lcdqr.py"
	try:
		res = requests.post("http://192.168.43.114:5000/check/", json=s).json()
		check = res['check']
		rec_file_name = res['file_name']
		rec_file_name_dir=os.path.join(os.getcwd(),res['file_name'])
		print (check)
		print (rec_file_name)
		print (rec_file_name_dir)
		
		if(res['url']==''):
			print ('File Not Found')
		else:
			print (res['url'])
			try:
				urllib.urlretrieve(res['url'],os.path.join(update_directory,rec_file_name_dir))
				print ("file retrieved")
				#process = "ps aux | grep \"[p]ython3 " + slave_file +"\" | awk \'{print $2}\'"
				#print(process)
				#sp.call(process,shell=True)
				#kill_proc = 'pkill -9 '+process[0]
				#sp.call(kill_proc, shell=True)
				#print("proc killed")
				os.remove(slave_file)
				print("file removed")
				shutil.move(os.path.join(update_directory,rec_file_name),os.getcwd())
				#os.rename(rec_file_name,slave_file)
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

for file in os.listdir('.'):
        if fnmatch.fnmatch(file, 'lcdqr*.py'):
                slave_file = file
check_update()
#cmd = "python3 " + slave_file
#sp.Popen(cmd, shell=True)
