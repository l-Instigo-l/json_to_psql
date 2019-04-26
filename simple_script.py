import json
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://postgres:skyline92@localhost/postgres')
db = scoped_session(sessionmaker(bind=engine))

def json_to_psql():
	#json_data = requests.get("http://url-to-api")
	#data = json_data.json()

	with open('json_data.json', 'r') as f:
	        data = json.load(f)

	Origin = data['Origin']
	Destination = data['Destination']
	Departure_date = data['Departure_Date']
	Customers_data = json.dumps(data['Customers_data'])

	print(Origin, Destination, Departure_date, Customers_data)

	db.execute("INSERT INTO test_table (origin, destination, departure_date, customers_data) VALUES (:origin, :destination, :departure_date, :customers_data)", {"origin": Origin, "destination": Destination, "departure_date": Departure_date, "customers_data": Customers_data})
	db.commit()

def psql_to_json(id):
	# Выбор строки таблицы осуществляется по id
	data = db.execute("SELECT * FROM test_table WHERE id = :id ", {"id": id}).fetchone()

	Origin = data.origin
	Destination = data.destination
	Departure_date = str(data.departure_date)
	Customers_data = data.customers_data

	d = { "Origin": Origin, "Destination": Destination, "Departure_Date" : Departure_date, "Customers_data": Customers_data}
	print(d)
	json_data = json.dumps(d)

	print(Origin, Destination, Departure_date, Customers_data)

psql_to_json(1)





