from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
#importa aqui las librerías para el control de los sensores de temeperatura.
import time
from datetime import datetime, timedelta, tzinfo
from decouple import config
import json
import random as rd #se importa para generar datos de prueba

app = Flask(__name__)

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['MYSQL_HOST'] = config('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(config('MYSQL_PORT'))
app.config['MYSQL_USER'] = config('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = config('MYSQL_PASS')
app.config['MYSQL_DB'] = config('MYSQL_DB')

mysql = MySQL(app)

cont = 0


def read_temperature():
    temperature = [
            {'idsensor_temperatura': 1, 'fecha_temperatura': datetime.now().strftime('%Y/%m/%d %H:%M:%S'), 'temperatura':rd.randint(0,150)},
            {'idsensor_temperatura': 2, 'fecha_temperatura': datetime.now().strftime('%Y/%m/%d %H:%M:%S'), 'temperatura':rd.randint(0,50)}
        ]
    return temperature


def insert_temperatura(temperature):
    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute('''INSERT INTO sensor_temperatura (idsensor_temperatura, fecha_temperatura, temperatura)
                        VALUES(%s,%s,%s)''',(temperature[0].get("idsensor_temperatura"),temperature[0].get("fecha_temperatura"),
                                                temperature[0].get("temperatura")))
            mysql.connection.commit()
            cursor.execute('''INSERT INTO sensor_temperatura (idsensor_temperatura, fecha_temperatura, temperatura)
                        VALUES(%s,%s,%s)''',(temperature[1].get("idsensor_temperatura"),temperature[1].get("fecha_temperatura"),
                                                temperature[1].get("temperatura")))
            mysql.connection.commit()
            cursor.close()
    except ValueError as e:
        mysql.connection.rollback()
        cursor.close()
        print(f'el error es {e}')

while cont <= 10:
    temperature = read_temperature()
    insert_temperatura(temperature)
    cont+=1
    print(cont)
    time.sleep(2)



