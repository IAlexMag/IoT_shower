from flask_mysqldb import MySQL
from decouple import config


def create_app():
    from flask import Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config('SECRET_KEY')
    app.config['MYSQL_HOST'] = config('MYSQL_HOST')
    app.config['MYSQL_PORT'] = int(config('MYSQL_PORT'))
    app.config['MYSQL_USER'] = config('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = config('MYSQL_PASS')
    app.config['MYSQL_DB'] = config('MYSQL_DB')
    return app
#print(app.config)


def conexion():
    app = create_app()
    mysql=MySQL(app)
    return mysql.connection