from logging import error
from consts import *
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from consts import error_template, success_template, user_template
import json

app = Flask(__name__)
app.config.from_object(Config)
my_db = SQLAlchemy(app)

from models.models import User, Data, create_token

my_db.create_all()

@app.route("/register/<name>", methods=['POST'])
def registerNewUser(name):
	if request.method != 'POST':
		return error_template.format(16)

	try:
		json_body = json.loads(request.get_data())
		new_user = User(\
			username=json_body['username'],\
			email=json_body['email'],\
			password_hashed=json_body['passsword_hashed'],\
			auth_token=None)
		if not User.contains_user_by_name(new_user.username):
			my_db.session.add(new_user)
			my_db.session.commit()
			return success_template.format('Registration successful', 'null')

		return error_template.format(18)
	except:
		return error_template.format(17)

@app.route("/login/<name>", methods=['POST'])
def loginUser(name):
	print(request.method)
	if request.method != 'POST':
		return error_template.format(16)

	if not User.contains_user_by_name(name):
		return error_template.format(19)

	try:
		client = json.loads(request.get_data())
		new_token = str(create_token())
		print(client)
		m_user = User.query.filter_by(username=name).first()
		if m_user.equals(client) and m_user.auth_token is not None:
			return error_template.format(20)

		m_user.auth_token = new_token
		my_db.session.commit()
		json_template = user_template.format(\
				m_user.username,\
				m_user.username,\
				m_user.password_hashed,\
				m_user.auth_token\
			)\

		print(json_template)
		return success_template.format(\
			'Successful logging in',\
			json_template
		)
	except:
		return error_template.format(17)

@app.route('/register/<name>', methods=['POST'])
def logoutUser(name):
	if request.method != 'POST':
		return error_template.format(16)
	
	if not User.contains_user_by_name(name):
		return error_template.format(19)

	try:
		m_user = User.query.filter_by(username=name).first()
		if m_user is None:
			return error_template.format(21)
		
		m_user.auth_token = None
		my_db.session.commit()
		return success_template.format('Successful logging out', 'null')
	except:
		return error_template.format(17)