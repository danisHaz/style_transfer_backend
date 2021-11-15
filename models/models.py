from enum import unique
from app import my_db
import os
import binascii
from consts import token_length

class User(my_db.Model):
	__tablename__ = 'user'

	id = my_db.Column(my_db.Integer, primary_key=True)
	username = my_db.Column(my_db.String(80), unique=True, nullable=False)
	email = my_db.Column(my_db.String(120), unique=True, nullable=False)
	password_hashed = my_db.Column(my_db.String(128), unique=False, nullable=False)
	auth_token = my_db.Column(my_db.String(token_length), unique=False, nullable=True)

	def __repr__(self) -> str :
		return f'{{"id": {self.id}, "username": "{self.username}", ' +\
			'"email": "{self.email}", "password_hashed": "{self.password_hashed}"}}'
	
	@staticmethod
	def contains_user_by_name(current_username: str) -> bool:
		if User.query.filter_by(username=current_username).first() is None:
			return False
	
	# cannot perform equality check by id because client doesn't have id of user
	def equals(self, user) -> bool:
		return (self.username == user.username)

class Data(my_db.Model):
	__tablename__ = 'data'

	id = my_db.Column(my_db.Integer, primary_key=True)
	user_id = my_db.Column(my_db.Integer, unique=False, nullable=False)
	data = my_db.Column(my_db.String, unique=False, nullable=False)

	def __repr__(self) -> str:
		return f'{{"id": {self.id}, "user_id": "{self.user_id}", "data": "{self.data}"}}'

def create_token() -> str:
	return binascii.hexlify(os.urandom(token_length // 2)).decode()