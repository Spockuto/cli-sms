#!/usr/bin/env python
import requests
import json
import sys
import os


API_KEY = os.environ.get('PUSHBULLET_TOKEN')
headers = {'Access-Token' : API_KEY}


print "Getting User Identifier..."
response = requests.get("https://api.pushbullet.com/v2/users/me", headers = headers)
source_user_iden = str(json.loads(response.text)['iden'])

print "Getting Mobile Identifier..."
response = requests.get("https://api.pushbullet.com/v2/devices", headers = headers)
response = json.loads(response.text)
for i , item in enumerate(response['devices']):
	print i , item['nickname']

count = input("Select a Mobile: ")
target_device_iden = str(response['devices'][count]['iden'])

print "Sending Sms"
final_data = {}
data = {}
data.update({"conversation_iden": "+91"+sys.argv[1]})
data.update({"message": sys.argv[2]})
data.update({"package_name": "com.pushbullet.android"})
data.update({"source_user_iden": source_user_iden})
data.update({ "target_device_iden": target_device_iden})
data.update({"type": "messaging_extension_reply"})
final_data.update({"push":data})
final_data.update({"type":"push"})

headers.update({'Content-Type': 'application/json'})
response = requests.post("https://api.pushbullet.com/v2/ephemerals", data = json.dumps(final_data) , headers = headers)

if response.text :
	print "Message Successfully Sent"
