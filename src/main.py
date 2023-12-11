from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from decouple import config
import bcrypt as bcp
import re

#configuraciones iniciales de la aplicación (conexión a BDD)
app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['MYSQL_HOST'] = config('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(config('MYSQL_PORT'))
app.config['MYSQL_USER'] = config('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = config('MYSQL_PASS')
app.config['MYSQL_DB'] = config('MYSQL_DB')

mysql = MySQL(app)
bcrypt=Bcrypt(app)

# rutas y funciones
@app.route('/')
def Index():
    return render_template('registro.html')


@app.route('/registro', methods=['POST'])
def registro():
    salt = bcp.gensalt()
    if request.method == 'POST':
        usuario = {'name': request.form['fname'],
         'lname': request.form['lname'],
         'mail': request.form['email'],
         'password': request.form['password'],
         'gender': request.form['gender']}
        usuario['password'] = bcp.hashpw(usuario.get('password').encode('utf-8'),salt)
        cur = mysql.connection.cursor()
        cur.execute(f'INSERT INTO {config("MYSQL_TABLE_USERS")} (first_name, last_name, email, contra, gender) VALUES (%s, %s, %s, %s, %s)',
                        (usuario.get("name"), usuario.get("lname"), usuario.get("mail"), usuario.get("password"), usuario.get("gender")))
        mysql.connection.commit()
    return redirect (url_for('login'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        inicio_sesion = {
            'email' : request.form['email'],
            'password' : request.form['password']
        }

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (inicio_sesion.get('email'),))
        user = cursor.fetchone()
        cursor.close()
        if user and bcrypt.check_password_hash(user[4], inicio_sesion.get('password')):
            session['user_id'] = user[0]
            return redirect(url_for('dash'))
        else:
            flash('Nombre de usuario o contraseña incorrecto', 'danger')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.pop('user_id', None)
        return redirect(url_for('login'))
    else:
        flash('Método no permitido para cerrar sesión', 'danger')
        return redirect(url_for('dash'))
    

@app.route('/dash')
def dash():
    if 'user_id' in session:
        return render_template('bao.html')
    else:
        return redirect(url_for('login'))

@app.route('/reset', methods = ['POST'])
def reset():
    if request.method == 'POST':
        return render_template('reset_pass.html')
    else:
        flash('Método inváido')
        return render_template('login.html')
# inicialización del servidor
if __name__ == '__main__':
    app.run(port = 5500, debug = True)

