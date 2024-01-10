from flask import Flask, render_template, url_for, jsonify
from flask_mysqldb import MySQL
from decouple import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['MYSQL_HOST'] = config('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(config('MYSQL_PORT'))
app.config['MYSQL_USER'] = config('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = config('MYSQL_PASS')
app.config['MYSQL_DB'] = config('MYSQL_DB')

mysql = MySQL(app)

def saludo_principal(id_user):
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT u.first_name, u.last_name,
                       msg.descripcion FROM users as u
                       LEFT JOIN cat_mensajes as msg 
                       ON u.id_mensaje = msg.id_mensaje where u.id_user = %s''', (id_user,))
        user = cursor.fetchone()
        cursor.close()
        name = f'{user[0]} {user[1]}'
        mensaje = user[2]
        return name, mensaje
        
        