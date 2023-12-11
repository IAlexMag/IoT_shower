'''from decouple import config
import pymysql

def get_connection():
    try:
        return pymysql.connect(
            host = config('MYSQL_HOST'),
            user = config('MYSQL_USER'),
            password = config('MYSQL_PASS'),
            db = config('MYSQL_DB')
        )
    except Exception as ex:
        print(ex)'''
