import json
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://username:password@localhost/postgres')
db = scoped_session(sessionmaker(bind=engine))

def json_to_psql():
	# Получение json через api
	#json_data = requests.get("http://url-api-endpoint")
	#data = json_data.json()

	# Чтение json из файла
	with open('json_data.json', 'r') as f:
	        data = json.load(f)

	Origin = data['Origin']
	Destination = data['Destination']
	Departure_date = data['Departure_Date']
	Customers_data = json.dumps(data['Customers_data']) # Данные в столбце Customers_data таблицы test_table, так же являются json-обьектом

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
	json_data = json.dumps(d)

	# Отправляем post-request и сохраняем ответ сервера
	r = requests.post(url = API_ENDPOINT, data = json_data) 





