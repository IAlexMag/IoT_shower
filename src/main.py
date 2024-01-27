from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from decouple import config
from flask_mail import Mail
from services.mailing import envio_mail
from services.dashboard import saludo_principal
from services.profile import info_users
from datetime import datetime, timedelta
from services.bano import sesion_bath
from threading import Thread
from services.PID_Completo import main
#from services.temperature import read_temperature
import bcrypt as bcp
import re
import random
import string

#configuraciones iniciales de la aplicación (conexión a BDD)
app = Flask(__name__)

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['MYSQL_HOST'] = config('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(config('MYSQL_PORT'))
app.config['MYSQL_USER'] = config('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = config('MYSQL_PASS')
app.config['MYSQL_DB'] = config('MYSQL_DB')

app.config['MAIL_SERVER'] = config('MAIL_SERVER')
app.config['MAIL_PORT'] = config('MAIL_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = config('USER_MAIL')
app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')

mysql = MySQL(app)
bcrypt=Bcrypt(app)
mail = Mail(app)

'''
def run_control(data):
    main(data)
'''
def handle_bad_request(error):
    response = jsonify({'message': 'Es necesario ingrese un genero'})
    response.status_code = 400
    return response

app.register_error_handler(400, handle_bad_request)

# rutas y funciones
@app.route('/', methods = ['GET', 'POST'])
def Index():
    if request.method == 'POST':
        return render_template('registro.html')
    else: 
        return render_template('registro.html')


@app.route('/registro', methods=['POST'])
def registro():
    salt = bcp.gensalt()
    try:
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
            cur.close()
        return redirect (url_for('login'))
    except ValueError as e:
        print(f'Error 400: {e}')
        return handle_bad_request(e)


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
        #print(user[15])
        if user and bcrypt.check_password_hash(user[4], inicio_sesion.get('password')):
            session['user_id'] = user[0]
            session['id_rol'] = user[15]

            if session['id_rol'] == 1:
                return redirect(url_for('dash_admin'))
            else:
                return redirect(url_for('dash'))
        else:
            flash('Nombre de usuario o contraseña incorrecto', 'danger')
            return render_template('login_2.html')
    else:
        return render_template('login_2.html')

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    if request.method == 'POST' or request.method == 'GET':
        session.pop('user_id', None)
        return redirect(url_for('login'))
    else:
        flash('Método no permitido para cerrar sesión', 'danger')
        return redirect(url_for('dash'))
    

@app.route('/dash')
def dash():
    if 'user_id' in session:
        id_user = session['user_id']
        name, mensaje = saludo_principal(id_user)
        return render_template('index.html', name = name, mensaje = mensaje)
    else:
        flash('es necesario inicie sesión')
        return redirect(url_for('login'))

@app.route('/dash_admin')
def dash_admin():
    if 'user_id' in session:
        return render_template('dashboard.html')
    else:
        flash('es necesario inicie sesión')
        return redirect(url_for('login'))

@app.route('/reset', methods = ['GET','POST'])
def reset():
    if request.method == 'POST' or request.method == 'GET':
        return render_template('reset_pass_2.html')
    else:
        flash('Método inváido')
        return render_template('login_2.html')

@app.route('/send_pass', methods = ['POST'])
def send_pass():
    if request.method == 'POST':
        mail = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (mail,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            mailing = user[3]
            name = user[1]
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            expiracion = datetime.utcnow() + timedelta(hours=1)
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE users SET token = %s, fecha_token = %s WHERE id_user = %s", (token, expiracion, user[0],))
            mysql.connection.commit()
            cursor.close()
            envio_mail(mailing,name, token)
            flash('Se ha enviado un enlace de recuperación a tu dirección registrada')
            return redirect(url_for('login'))
        else:
            flash('No se ha encontrado un usario con el correo proporcionado')
            return redirect(url_for('login'))
    else:
        flash('Método inválido')
        return render_template('login_2.html')

@app.route('/recuperar/<token>', methods = ['GET', 'POST'])
def recuperar(token):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users where token = %s AND fecha_token > NOW()", (token,))
    user = cursor.fetchone()
    cursor.close()
    #print(user)


    if user:
        if request.method == 'POST':
            salt = bcp.gensalt()
            new_pass = bcp.hashpw(request.form['new_pass'].encode('utf-8'),salt)
            #print(new_pass)
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE users SET contra = %s WHERE id_user = %s", (new_pass, user[0],))
            mysql.connection.commit()
            cursor.close()
            #return render_template('/recuperar_contra.html')
            flash('se ha reestablecido la contraeña de forma exitosa')
            return redirect(url_for('login'))
        else:
            return render_template('recuperar_contra.html', token = token)
    else:
        return redirect(url_for('login'))
    
'''
@app.route("/temperature", methods = ['GET'])
def get_temp():
    temp = 
'''

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' in session:
        id_user = session['user_id']
        mail, name, apaterno, amaterno = info_users(id_user)
        return render_template('Perfil.html', mail = mail, name = name, apaterno = apaterno,
                               amaterno=amaterno)
    else:
        return redirect(url_for('login'))

@app.route('/bano', methods= ['GET'])
def bano():
    if 'user_id' in session:
        id_user = session['user_id']
        return render_template('Bano.html')
    else:
        return redirect(url_for('login'))
@app.route('/pro_bano', methods = ['GET','POST'])
def pro_bano():
     if request.method == 'POST' and 'user_id' in session:
        data = request.get_json()
        print(data)
        id_user = session['user_id']
        sesion_bath(data, id_user)
        #params_pid(data)
        main(data)
        #control_thread = Thread(target=run_control, args=(data,))
        #control_thread.start()
        #flash('Se ha programado tu baño con éxito')
        return jsonify({'message': 'Se ha programado tu baño con éxito',
                        'params': data})
     else:
         #flash('Necesitas programar tu baño')
         return jsonify({'message': 'necesitas programar tu baño'})

@app.route('/ducha_pro', methods=['GET'])
def ducha():
    if 'user_id' in session:
        id_user = session['user_id']
        return render_template('Ducha.html')
    else:
        return redirect(url_for('login'))


@app.route('/info', methods=['GET'])
def info():
    if 'user_id' in session:
        id_user = session['user_id']
        return render_template('informacion.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/conexion', methods=['GET'])
def conect():
    if 'user_id' in session:
        id_user = session['user_id']
        return render_template('Conexion.html')
    else:
        return redirect(url_for('login'))
# inicialización del servidor
if __name__ == '__main__':
    mail.init_app(app)
    app.run(host='0.0.0.0', port = 7405, debug = True)

