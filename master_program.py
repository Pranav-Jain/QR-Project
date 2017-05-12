#!/usr/bin/env python

import subprocess as sp
import urllib
import threading
import sys
import json
import requests
import urllib
import glob

global slave_file
slave_file = glob.glob('lcdqr*.py')
def check_update():
	remote_file = "test.py"
	file = [{'input': remote_file}]
	s = json.dumps(file)
	#global slave_file = "lcdqr.py"
	try:
		res = requests.post("http://127.0.0.1:5000/check/", json=s).json()
		check = res['check']
		print check
		if(res['url']==''):
			print 'File Not Found'
		else:
			print res['url']
			try:
				urllib.urlretrieve(res['url'])
				print ("file retrieved")
				command = 'ps aux | grep ' +'\'Python ' + slave_file + '\''
				process = sp.call(command, shell = True)
				
			except:
				pass
		#os.remove(slave_file)
	except:
		pass
	threading.Timer(5, check_update).start()	


check_update()
cmd = "python3 " + slave_file
sp.Popen(cmd, shell=True)