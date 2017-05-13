from flask import Flask
from flask import request
from flask import send_from_directory
import json
import subprocess as sp
from ftplib import FTP 
import os.path
import os

app = Flask(__name__) 

@app.route('/check/', methods = ['POST'])
def check():
	jsondata = request.get_json()
	data = json.loads(jsondata)					
	file = 'slave1.py'
	print data
	x = os.path.isfile(data[0]['input'])
	print data[0]['mac']
	print data[0]['time']
	url=''
	file_url='file'
	if(x==False):
		url = 'http://192.168.1.102:5000/' + file_url

	result = {'check':not x,'url':url, 'file_name':file}
	return json.dumps(result)

@app.route('/<file_url>')
def file(file_url):
	return send_from_directory(directory=os.path.join(os.getcwd(), 'update'), filename='slave1.py', as_attachment=True)

#@app.route('/register')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)