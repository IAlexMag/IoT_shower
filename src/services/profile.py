from flask import Flask, render_template, redirect, jsonify
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

def info_users(id_user):
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT email, first_name, TRIM(SUBSTRING_INDEX(last_name, ' ', 1)) as APaterno,
                       TRIM(SUBSTRING_INDEX(last_name, ' ',-1)) as AMaterno FROM users
                       WHERE id_user = %s''', (id_user,))
        user = cursor.fetchone()
        cursor.close()
        mail = user[0]
        name = user[1]
        apaterno = user[2]
        amaterno = user[3]
        return mail, name, apaterno, amaterno
    
def modify_user(id_user):
    with app.app_context():
        pass


        