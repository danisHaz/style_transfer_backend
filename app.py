from logging import error
from consts import *
from flask import request
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)
my_db = SQLAlchemy(app)

from models.models import User, Data, create_token

my_db.create_all()

@app.route("/register/<name>", methods=['POST'])
def registerNewUser(name):
	if request.method != 'POST':
		return error_template.format('Wrong query to database')

	try:
		json_body = json.loads(request.get_data())
		new_user = User(\
			username=json_body['username'],\
			email=json_body['email'],\
			password_hashed=json_body['passsword_hashed'],\
			auth_token=None)
		if not User.contains_user_by_name(new_user.username):
			User.session.add(new_user)
			return success_template.format('Registration successful', 'null')

		return error_template.format('User is already registered')
	except:
		return error_template.format('Invalid data passed to body')

@app.route("/login/<name>", methods=['POST'])
def loginUser(name):
	if request.method != 'POST':
		return error_template.format('Wrong query to database')
	if not User.contains_user_by_name(name):
		return error_template.format('User is not registered')

	try:
		client = json.loads(request.get_data())
		new_token = str(create_token())
		m_user = User.query.filter_by(username=name).first()
		if m_user.equals(client):
			return error_template.format('User is already logged in')
		
		m_user.auth_token = new_token
		my_db.session.commit()
		return success_template.format(\
			'Successful logging in',\
			user_template.format(\
				m_user.username,\
				m_user.username,\
				m_user.password_hashed,\
				m_user.auth_token\
			)\
		)
	except:
		return error_template.format('Invalid data passed to body')

@app.route('/register/<name>', methods=['POST'])
def logoutUser(name):
	if request.method != 'POST':
		return error_template.format('Wrong query to database')
	
	if not User.contains_user_by_name(name):
		return error_template.format('User is not registered')

	try:
		m_user = User.query.filter_by(username=name).first()
		if m_user is None:
			return error_template.format('Provided username does not exist')
		
		m_user.auth_token = None
		my_db.session.commit()
		return success_template.format('Successful logging out', 'null')
	except:
		return error_template.format('Invalid data passed to body')

# admin = User(username='admin', email='admin@example.com', password_hashed='hdahduaidhs', auth_token=None)
# guest = User(username='guest', email='guest@example.com', password_hashed='hdahduaidhs', auth_token=None)
# my_db.session.add(admin)
# my_db.session.add(guest)