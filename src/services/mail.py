import smtplib
from decouple import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


remitente = config('USER_MAIL')
destinatario = 'alexander_orenda@outlook.com' #esta variable será reemplazada por el valor obtenido en el query de búsqueda
asunto = 'TEST'

msg = MIMEMultipart()
msg['subject'] = asunto
msg['From'] = remitente
msg['To'] = destinatario

# se hará la conexión a la base de datos mediante librería flask o librerías relacionadas con MYSQL

# función que recibirá el parámetro de correo electrónico y hará el query de búsqueda.

with open ('src/Templates/email.html', 'r') as archivo:
    html = archivo.read()

# adjunta el contenido html
msg.attach(MIMEText(html, 'html'))

#conexión con un servidor de correo eletrónico saliento (SMTP)
server = smtplib.SMTP('smtp.gmail.com', 587)
# conexión segura
server.starttls()
server.login(remitente, config('MAIL_PASSWORD'))

#enviar correo eletrónico

server.sendmail(remitente, destinatario, msg.as_string())

server.quit()