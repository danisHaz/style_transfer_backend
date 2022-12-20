import sys
import ast

from consts import *
from flask import Flask, request
import sqlalchemy
from config import Config
from consts import Templates
from models.models import User, StaticQueries, create_token
import numpy as np
import json
from models.connection import Connection

app = Flask(__name__)
app.config.from_object(Config)
my_db = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = Connection(my_db.connect())


@app.route("/<email>", methods=['GET'])
def getClientData(email):
	return str(connection.get_data_from_table(connection, 'select * from PlaneState'))

@app.route("/newEmployees", methods=['GET'])
def getNewEmployees():
	return str(connection.get_data_from_table(connection, "meme"))

@app.route("/login", methods=["POST"])
def performLoginUser():
	json_body = json.loads(request.get_data())
	new_user = User(\
		email=json_body['email'],\
		password=json_body['password'])
	
	data = None
	if new_user.phone_number is not None:
		data = connection.get_data_from_table(StaticQueries.check_user_by_phone.format(new_user.phone_number, new_user.password))
	elif new_user.email is not None:
		data = connection.get_data_from_table(StaticQueries.check_user_by_email.format(new_user.email, new_user.password))

	if data is None or data[0][0] == 0:
		return Templates.error_template.format(error_codes[19])
	else:
		return Templates.success_template.format("successfully logged in", Templates.user_template.format(new_user.email, "true"))


@app.route("/register/<name>", methods=['POST'])
def registerNewUser(name):
	if request.method != 'POST':
		return Templates.error_template.format(16)

	try:
		json_body = json.loads(request.get_data())
		print(json_body)
		new_user = User(\
			username=json_body['username'],\
			email=json_body['email'],\
			password_hashed=json_body['password'],\
			auth_token=None)
		if not User.contains_user_by_name(new_user.username):
			my_db.session.add(new_user)
			my_db.session.commit()
			return Templates.success_template.format('Registration successful', 'null')

		return Templates.error_template.format(18)
	except:
		return Templates.error_template.format(17)

@app.route("/login/<name>", methods=['POST'])
def loginUser(name):
	print(request.method)
	if request.method != 'POST':
		return Templates.error_template.format(16)

	if not User.contains_user_by_name(name):
		return Templates.error_template.format(19)

	try:
		client = json.loads(request.get_data())
		new_token = str(create_token())
		print(client)
		m_user = User.query.filter_by(username=name).first()
		if m_user.equals(client) and m_user.auth_token is not None:
			return Templates.error_template.format(20)

		m_user.auth_token = new_token
		my_db.session.commit()
		json_template = Templates.user_template.format(\
				m_user.username,\
				m_user.username,\
				m_user.password_hashed,\
				m_user.auth_token\
			)\

		print(json_template)
		return Templates.success_template.format(\
			'Successful logging in',\
			json_template
		)
	except:
		return Templates.error_template.format(17)

@app.route('/register/<name>', methods=['POST'])
def logoutUser(name):
	if request.method != 'POST':
		return Templates.error_template.format(16)
	
	if not User.contains_user_by_name(name):
		return Templates.error_template.format(19)

	try:
		m_user = User.query.filter_by(username=name).first()
		if m_user is None:
			return Templates.error_template.format(21)
		
		m_user.auth_token = None
		my_db.session.commit()
		return Templates.success_template.format('Successful logging out', 'null')
	except:
		return Templates.error_template.format(17)