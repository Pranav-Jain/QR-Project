from flask import Flask
from flask import request
from flask import send_from_directory
import json
import subprocess as sp
from ftplib import FTP 
import os.path

app = Flask(__name__) 

@app.route('/check/', methods = ['POST'])
def check():
	jsondata = request.get_json()
	data = json.loads(jsondata)						#file = [{'input': 'file.txt'}, {'hjv':True}]
	
	x = os.path.isfile(data[0]['input'])
	url=''
	if(x==True):
		url = 'http://127.0.0.1:5000/file'

	result = {'check':x,'url':url}
	return json.dumps(result)

@app.route('/file')
def file():
	return send_from_directory(directory='/Users/pranavjain/Desktop', filename='file.txt', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)