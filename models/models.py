import os
import binascii
from consts import token_length

class User:
	__tablename__ = 'User'

	def __init__(self, user_id = None, phone_number = None, 
		email = None, country_code = None, name = None, surname = None, password = None):

		self.user_id = user_id
		self.phone_number = phone_number
		self.email = email
		self.country_code = country_code
		self.name = name
		self.surname = surname
		self.password = password

	def __repr__(self) -> str :
		return f'{{"user_id": {self.id}, "phone_number": "{self.phone_number}", ' +\
			'"email": "{self.email}", "country_code": "{self.country_code}", ' +\
			'"name": "{self.name}", "surname": "{self.surname}", "password": "{self.password}"}}'
	
	@staticmethod
	def contains_user_by_name(current_username: str) -> bool:
		if User.query.filter_by(username=current_username).first() is None:
			return False
		return True
	
	@staticmethod
	def get_user_data_by_email(current_email: str) -> str:
		data = User.query.filter_by(email=current_email).first()
		if data is None:
			raise Exception
		
		return str(data)
	
	# cannot perform equality check by id because User doesn't have id of user
	def equals(self, user) -> bool:
		return (self.username == user['username'])

def create_token() -> str:
	return binascii.hexlify(os.urandom(token_length // 2)).decode()

class StaticQueries:
	get_new_employees = 'select employee_name, employee_surname from Employees ' +\
		'where employee_id not in (' +\
		'select employee_id from aviasales.PlaneState);'
	
	check_user_by_phone = 'select count(client_id) from Client where phone_number = "{}" and password = MD5("{}");'
	check_user_by_email = 'select count(client_id) from Client where email = "{}" and password = MD5("{}");'