import requests
import json
from random import randrange
import random
from random import randrange
from random import randint
import array
import pandas as pd
import string

def string_generator(size=7):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

def Signup():
	print("Signing Up")  
	url = 'https://fiberdemoms.embibe.com/user_auth/auth/sign_in'
	header = 'Content-Type: application/json'
	password = "embibe1234"
	res = string_generator(8)
	signup_data = {"login":"test_user_"+res+"@gmail.com","password":password, "flag":"sp"}
	# print("dankja")
	response = requests.post(url, data=json.dumps(signup_data))

	print("\t",response)
	json_dict = json.loads(response.text)
	print("\tUser signed up")
	print("\tEmail: ","test_user_"+res+"@gmail.com")
	print("\tPassword: ",password)
	print("\tId: ",json_dict['resource']['id'])

	return json_dict['resource']['email'],json_dict['resource']['id']

def login(email_id,password):
	print("\nUser Logging In")
	url = 'https://fiberdemoms.embibe.com/user_auth/auth/sign_in'
	header = 'Content-Type: application/json'
	# rnum = randrange(len(email_password)-1)
	login_data={
				"login": email_id,
				"password":password
			 }
	response = requests.post(url, data=json.dumps(login_data))
	# print("\t",response)
	# print(response.headers)
	json_dict = json.loads(response.text)
	# print(json_dict)
	print("\tUser logged in")
	print("\tEmail: ",email_id)
	print("\tPassword: ",password)
	print("\tembibe-token: ",response.headers['embibe-token'])
	return json_dict['resource']['grade'],response.headers['embibe-token']

def add_user(parent_id,grade):
	print("\nAdding new user(child)")
	if (parent_id != None and parent_id != ''):
		# res = string_generator(6)
		url = "https://fiberdemoms.embibe.com/user_auth/add?id="+str(parent_id) 
		header = 'Content-Type: application/json'

		res = string_generator(7)
		child_email_id = "loadtestchild"+res+"@gmail.com"
		user_data = {
			"parent_id": parent_id,
			"first_name": "Test",
			"user_type" : "child",
			"email_id" : child_email_id,
			"goal" : "g10",
			"current_grade" : "10",
			"school" : "DPS",
			"avatar_image" : "S3 Url (String)"
		}
		response = requests.post(url, data=json.dumps(user_data))
		# print("\t",response)
		# print(response.text)
		json_dict = json.loads(response.text)      
		# print(json_dict)
		print("\tNew child added")
		print("\tchild_id: ",json_dict["child_id"])
		print("\tchild_emailid: ",child_email_id)
		return json_dict["child_id"],child_email_id


# signup_data = Signup()
# login_data = login(signup_data[0],"embibe1234")
# user_data = add_user(signup_data[1],login_data[0])


