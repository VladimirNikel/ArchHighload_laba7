from typing import Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

import uvicorn

#необходимо, чтобы работать с json'ом
import json

#необходимо для работы с переменными окружения
import os
import sys

#необходимо для работы с API openweathermap
import pyowm
from pyowm.utils.config import get_default_config
from pyowm.utils import timestamps

import rediscluster

#задание параметров redis'а
redis_host, redis_port, redis_db = '194.61.2.84', 6379, 0

rc = rediscluster.RedisCluster(startup_nodes=[{"host": redis_host, "port": redis_port}], decode_responses=True)

time_storage = 60*10				#10 минут - актуальность данных о погоде в городе

config_dict = get_default_config()
config_dict['language'] = 'ru'

app_key = os.environ.get('OWM_APP_KEY')
owm = pyowm.OWM(app_key, config_dict)

my_id = sys.argv[1]

def current_weather(city: str):
	#обращение к внешнему сервису
	mgr = owm.weather_manager()
	observation = mgr.weather_at_place(city)
	w = observation.weather
	temp = w.temperature('celsius')['temp']

	#занесение в бд данных
	rc.set(city, temp, ex=time_storage)

	#возвращение текущей погоды
	return temp

def forecast_weather(city: str, timestamp: str):
	#обращение к внешнему сервису
	mgr = owm.weather_manager()
	observation = mgr.forecast_at_place(city, "3h") #данной командой стягивается прогноз погоды на ближайшие 5 дней с частотой 3 часа
	if timestamp == "1h":
		time = timestamps.next_hour()
	elif timestamp == "3h":
		time = timestamps.next_three_hours() 
	else:
		time = timestamps.now();
	w = observation.get_weather_at(time)
	temp = w.temperature('celsius')['temp']

	#занесение в бд данных (не совсем корректно, ведь у нас прогноз погоды...)
	rc.set(city, temp, ex=time_storage)

	#возвращение текущей погоды
	return temp

#кто будет читать и использовать код ниже: простите меня ;) костыль еще тот... надо было через nginx делать
def find_data(city: str, metod: bool, ts: str):
	if type(rc.get(city)) != type(None):
		#если в базе найдено значение
		print("city: ",city," взято из кэша и актуально: ", rc.ttl(city))
		return rc.get(city)
	else:
		#если не найдено значение
		print("city: ",city," ищем в API")
		if metod == True:	#current weather
			return current_weather(city)
		else:				#forecast weather
			return forecast_weather(city, ts)

@app.get("/")
def print_web():
	html_content = open('./index.html', 'r').read()
	return HTMLResponse(content=html_content, status_code=200)

@app.get("/v1/current/")
def current(city: str):
	temp = find_data(city.lower(), True, "")
	return json.dumps({"city": city,"unit": "celsius", "temperature": temp, "id_service": my_id})

@app.get("/v1/forecast/")
def forecast(city: str, timestamp: str):
	temp = find_data(city.lower(), False, timestamp)
	return json.dumps({"city": city,"unit": "celsius", "temperature": temp, "id_service": my_id})

if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=8000)
	pool.release(client)