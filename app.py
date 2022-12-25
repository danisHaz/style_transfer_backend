import sys
import ast

from consts import *
from flask import Flask, request
import sqlalchemy
from config import Config
from consts import Templates
from models.models import User, StaticQueries, create_token, Flight, Order
import numpy as np
import json
from models.connection import Connection

app = Flask(__name__)
app.config.from_object(Config)
my_db = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = Connection(my_db)

@app.route("/login", methods=["POST"])
def performLoginUser():
	json_body = json.loads(request.get_data())
	new_user = User(\
		email=json_body['email'],\
		password=json_body['password'])

	print(new_user.email)
	
	data = None
	if new_user.phone_number is not None:
		data = connection.get_data_from_table(StaticQueries.check_user_by_phone.format(new_user.phone_number, new_user.password))
	elif new_user.email is not None:
		data = connection.get_data_from_table(StaticQueries.check_user_by_email.format(new_user.email, new_user.password))
	
	print(data)

	if data is None or len(data) == 0:
		return Templates.error_template.format(error_codes[19])
	else:
		return Templates.success_template.format("successfully logged in", Templates.user_template.format(data[0][0], new_user.email, "true"))

@app.route("/popularTakeoffs", methods=["GET"])
def retrievePopularTakeoffs():
	data = connection.get_data_from_table(StaticQueries.get_popular_takeoff.format('2022-12-01 00:00:00', '2023-02-28 23:59:59'))
	print(data)
	if len(data) == 0 or len(data[0]) == 0:
		return Templates.error_template.format(error_codes[19])
	
	res = "[\n"
	for d in range(len(data)):
		res += Templates.takeoff_template.format(
			data[d][0], data[d][1], data[d][2], data[d][3], data[d][4]
		)
		if d == len(data) - 1:
			res += '\n'
		else:
			res += ',\n'
	res += ']'

	print(res)
	return res

@app.route("/findByFilterQuery", methods=["POST"])
def findByFilterQuiery():
	json_body = json.loads(request.get_data())
	print(json_body)
	flight = Flight(
		city_name_from=json_body['city_name_from'],
		city_name_to=json_body['city_name_to'],
		time_from=json_body['time_from'],
		time_to=json_body['time_to'])

	data = connection.get_data_from_table(StaticQueries.find_by_filter_quiery.format(
		flight.time_from, flight.time_to, flight.city_name_from, flight.city_name_to
	))

	if len(data) == 0:
		return '[]'

	res = '['

	for d in data:
		res += Flight(d[1], d[2], d[3], d[4], d[0]).toJson() + ',\n'
	
	res = res[:-2] + ']'
	print(res)
	return res

@app.route("/getCities")
def getCities():
	data = connection.get_data_from_table(StaticQueries.get_cities)
	res = '['
	for d in range(len(data)):
		if d == len(data) - 1:
			res += '"' + data[d][0] + '"'
		else:
			res += '"' + data[d][0] + '", '
	res += ']'

	print(res)
	return res

@app.route("/getTicketData", methods=['POST'])
def getTicketData():
	json_body = json.loads(request.get_data())
	print(json_body)
	timetable_id = json_body

	print("timetable", timetable_id)

	data = connection.get_data_from_table(StaticQueries.buy_ticket_data.format(timetable_id))

	print(data)

	if data is None or len(data) == 0:
		return Templates.error_template.format(error_codes[16])
	
	ticket = min(data, key=lambda a: a[5])

	print(ticket)

	return Templates.buy_ticket_template.format(*ticket)

@app.route("/addToOrderHistory", methods=['POST'])
def addToOrderHistory():
	json_body = json.loads(request.get_data())
	print(json_body)
	order = Order(
		json_body['clientId'],
		json_body['timeFrom'],
		json_body['timeTo'],
		json_body['cityCodeFrom'],
		json_body['cityCodeTo'],
		json_body['seatNumberId'],
		json_body['price'],
		json_body['orderTime'],
		json_body['planeFactoryId'],
		json_body['status'],
		json_body['hadLuggage'],
		json_body['timetableId']
	)

	print("Order", order.timetableId)

	data = connection.get_data_from_table(StaticQueries.get_plane_flight_id_by_timetable_id.format(order.timetableId))

	if data is None or len(data) == 0:
		return Templates.error_template.format(error_codes[17])

	plane_flight_id = data[0][0]
	
	print(order)

	connection.execute_query(StaticQueries.set_available_to_zero.format(plane_flight_id, order.seatNumberId))
	connection.execute_query(StaticQueries.update_whole_available_seats.format(plane_flight_id))
	connection.execute_query(StaticQueries.update_base_available_seats.format(plane_flight_id))
	connection.execute_query(StaticQueries.add_to_order_history.format(
		order.clientId,
		order.timeFrom,
		order.timeTo,
		order.cityCodeFrom,
		order.cityCodeTo,
		order.seatNumberId,
		order.price,
		order.orderTime,
		order.planeFactoryId,
		order.status,
		order.hadLuggage,
		order.timetableId
	))
	return Templates.success_template.format("OK", 1)

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