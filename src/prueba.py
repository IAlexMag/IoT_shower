from flask import Flask
from database.db import conexion
#from flask_mysqldb import MySQL
#from decouple import config
#import pandas as pd
#import numpy as np


app = Flask(__name__)

print(app.config)

@app.route('/')
def index():
    id = 3
    with app.app_context():
        db = conexion()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE id_user = %s',(id,))
        user = cursor.fetchone()
        cursor.close()
    return str(user)

if __name__ == '__main__':
    app.run(port=9900, debug=True)


'''

df = pd.read_csv('src/utils/data/sensor_temperatura.csv')
df['idsensor_temperatura'] = 1
df['id_user'] = 3

df_1 = pd.DataFrame(df, columns = ["idsensor_temperatura", "idsesiones_de_bano", "fecha_temperatura", "temperatura", "id_user"])

data = [tuple(x) for x in df_1.to_numpy()]

with app.app_context():
    cursor = mysql.connection.cursor()
'''

 #   cursor.executemany('''INSERT INTO sensor_temperatura (idsensor_temperatura, idsesiones_de_bano, fecha_temperatura, temperatura, id_user)
                #    VALUES (%s,%s,%s,%s,%s)''',data)

  #  mysql.connection.commit()

   # cursor.close()