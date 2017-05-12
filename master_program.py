#!/usr/bin/env python

import subprocess as sp
import urllib
import threading
global slave_file
slave_file = "lcdqr.py"
def check_update():
	remote_file = "test.py"
	ota_addr="ftp://0.0.0.0:2121/"+remote_file
	#global slave_file = "lcdqr.py"
	try:
		urllib.urlretrieve(ota_addr, remote_file)
		slave_file = remote_file
		print ("file retrieved")
		#os.remove(slave_file)
	except:
		pass
	threading.Timer(5, check_update).start()	


check_update()
cmd = "python3 " + slave_file
sp.Popen(cmd, shell=True)