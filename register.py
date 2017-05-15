#!/usr/bin/env python
import time
import datetime
import json
import requests
from uuid import getnode as get_mac

file = [{'mac':str(get_mac()),'time':datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}]
s = json.dumps(file)
for i in range(5):
    print("in for loop")
    res = requests.post("http://192.168.1.106:5000/register/", json=s).json()
    print(str(get_mac()))
    print("try: "+str(i))
    if (str(res['reg_status'])=='register ok'):
        print((res['reg_status']))
        break
    
