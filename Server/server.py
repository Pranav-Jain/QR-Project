from flask import Flask
from flask import request
import requests
from flask import send_from_directory
import json
import subprocess as sp
from ftplib import FTP 
import os.path
#import os

app = Flask(__name__) 

@app.route('/check/', methods = ['POST'])
def check():
	jsondata = request.get_json()
	data = json.loads(jsondata)					
	file = 'slave1.py' #can be changed
	url=''
	status = ''
	#print data

	with open("Mac ID.txt", "r") as f:
		macs = f.readlines()
	#print macs
	if data[0]['mac']+ '\n' not in macs:
		status='not registered'
	else:
		status='registered'
	x = False
	if status=='registered':
		x = os.path.isfile("./update/"+data[0]['current_file_name']) #put meaningful name
		file_url='file' #can be shifted, update_file url, can be made global too
		if(x==False):
			url = 'http://192.168.1.106:5000/file/' + file_url

	result = {'update_flag':not x,'url':url, 'file_name':file, 'reg_status':status}
	return json.dumps(result)

@app.route('/register/', methods=['POST'])
def register():
	jsondata = request.get_json()
	data = json.loads(jsondata)
	with open("Mac ID.txt", "r") as f:
		macs = f.readlines()
	f = open("Mac ID.txt", "ab+")
	print macs
	if data[0]['mac']+"\n" not in macs:
		f.write(str(data[0]['mac']) + '\n')
		f.flush()
		return json.dumps({'reg_status':'register ok'})
	else:
		return json.dumps({'reg_status':'Registered'})
	f.close()

@app.route('/file/<file_url>')
def file(file_url):
	return send_from_directory(directory=str(os.path.join(os.getcwd(), 'update')), filename='slave1.py', as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
