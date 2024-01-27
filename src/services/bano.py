from flask import Flask, redirect, jsonify, request
from flask_mysqldb import MySQL
from decouple import config
from datetime import datetime, timedelta
import random as rd

app = Flask(__name__)

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['MYSQL_HOST'] = config('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(config('MYSQL_PORT'))
app.config['MYSQL_USER'] = config('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = config('MYSQL_PASS')
app.config['MYSQL_DB'] = config('MYSQL_DB')

mysql = MySQL(app)

modos_bano = {
    'relax' : 1,
    'fast' : 2,
    'hot' : 3,
    'ahorro' : 4,
    'cool' : 5,
    'smart' : 6
}

start_date = datetime.now()


def sesion_bath(data, id_user):
    # empieza a generar la sesión de baño
    with app.app_context():
        mood = data.get("tipo_bano")
        id_modo = modos_bano.get(mood)
        end_date = start_date + timedelta(minutes=int(data.get("duracion",0)))
        duracion = int(data.get("duracion", 0))
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO sesiones_de_bano (id_modo_bano, id_user, temperatura,
                        duracion_est,
                       start_date, end_date, idtipos_sesiones, idestatus_sesion)
                       VALUES(%s, %s, %s, %s, %s, %s, %s, %s)''', (id_modo, id_user,
                                                                   int(data.get("temperature",0)),
                                                                   timedelta(minutes=duracion),
                                                                   start_date,
                                                                   end_date,
                                                                   1,
                                                                   1
                                                                   ))
        mysql.connection.commit()
        cursor.close()
    return print(f'se ha programado con éxito el baño con parametros: {data}')


def params_pid(data):
    return data
