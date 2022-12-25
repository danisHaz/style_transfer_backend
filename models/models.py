import os
import binascii
from consts import token_length
from consts import Templates

class User:
	__tablename__ = 'Client'

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

class Flight:
	__tablename__ = 'TimeTable'
	def __init__(self, city_name_from, city_name_to, time_from, time_to, timetable_id = None) -> None:
		self.city_name_from = city_name_from
		self.city_name_to = city_name_to
		self.time_from = time_from
		self.time_to = time_to
		self.timetable_id = timetable_id
	
	def toJson(self):
		return Templates.takeoff_template.format(
			self.timetable_id,
			self.city_name_from,
			self.city_name_to,
			self.time_from,
			self.time_to
		)

class Order:
	def __init__(self, clientId, timeFrom, timeTo, cityCodeFrom,\
		cityCodeTo, seatNumberId, price, orderTime, planeFactoryId,\
		status, hadLuggage, timetableId):
		self.clientId = clientId
		self.timeFrom = timeFrom
		self.timeTo = timeTo
		self.cityCodeFrom = cityCodeFrom
		self.cityCodeTo = cityCodeTo
		self.seatNumberId = seatNumberId
		self.price = price
		self.orderTime = orderTime
		self.planeFactoryId = planeFactoryId
		self.status = status
		self.hadLuggage = hadLuggage
		self.timetableId = timetableId


class StaticQueries:
	get_new_employees = 'select employee_name, employee_surname from Employees ' +\
		'where employee_id not in (' +\
		'select employee_id from aviasales.PlaneState);'
	
	check_user_by_phone = 'select client_id from Client where phone_number = "{}" and password = MD5("{}");'
	check_user_by_email = 'select client_id from Client where email = "{}" and password = MD5("{}");'

	get_popular_takeoff = '''
		select main_q.timetable_id, c1.city_name, c2.city_name, main_q.time_from, main_q.time_to, main_q.count_client
		from (
			select city_code_from, city_code_to, timetable_id, count(client_id) as count_client, time_from, time_to
			from aviasales.OrderHistory
			group by city_code_from, city_code_to, time_from, time_to, timetable_id
		) as main_q
		left join aviasales.Cities as c1 on main_q.city_code_from = c1.city_id
		left join aviasales.Cities as c2 on main_q.city_code_to = c2.city_id 
		where main_q.time_from >= '{}' and main_q.time_to <= '{}'
		group by c1.city_name, c2.city_name, main_q.count_client, main_q.time_from, main_q.time_to, main_q.timetable_id
		order by main_q.count_client desc;
	'''

	get_cities = 'select city_name from aviasales.Cities;'

	find_by_filter_quiery = '''
		select main_q.timetable_id, c1.city_name, c2.city_name, main_q.time_from, main_q.time_to
		from (
			select city_code_from, city_code_to, timetable_id, time_from, time_to
			from aviasales.TimeTable
		) as main_q
		left join aviasales.Cities as c1 on main_q.city_code_from = c1.city_id
		left join aviasales.Cities as c2 on main_q.city_code_to = c2.city_id 
		where main_q.time_from >= '{}' and main_q.time_to <= '{}' and c1.city_name = '{}' and c2.city_name = '{}';
	'''

	buy_ticket_data = '''
		select TT.time_from, TT.time_to, TT.city_code_from, TT.city_code_to,
			SS.default_price, SS.luggage_extra_amount, SS.seat_number_id, PS.plane_factory_id,
			C1.city_name, C2.city_name
		from TimeTable as TT
		inner join SeatState as SS on TT.plane_flight_id = SS.plane_flight_id
		inner join PlaneState as PS on TT.plane_flight_id = PS.plane_flight_id
		inner join Cities as C1 on C1.city_id = TT.city_code_from
		inner join Cities as C2 on C2.city_id = TT.city_code_to
		where TT.timetable_id = {} and SS.is_available = 1;
	'''

	get_plane_flight_id_by_timetable_id = '''
		select plane_flight_id from TimeTable where timetable_id = {};
	'''

	set_available_to_zero = '''
		update SeatState set is_available = 0 where plane_flight_id = {} and seat_number_id = {};
	'''

	update_whole_available_seats = '''
		update PlaneState set plane_whole_available_seats = plane_whole_available_seats - 1 where plane_flight_id = {};
	'''

	update_base_available_seats = '''
		update PlaneState set plane_base_available_seats = plane_whole_available_seats - 1 where plane_flight_id = {};
	'''

	add_to_order_history = '''
		insert into OrderHistory(client_id, time_from, time_to, city_code_from,
		city_code_to, seat_number_id, price, order_time, plane_factory_id,
		status, had_luggage, timetable_id) values ({}, "{}", "{}", {}, {}, {}, {}, "{}", {}, "{}", {}, {});
	'''
