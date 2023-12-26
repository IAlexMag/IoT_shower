# envío de correos electrónicos con flask

from flask import Flask, render_template, url_for
from flask_mail import Mail, Message
from decouple import config

mail = Mail()

def envio_mail(mailing, name, token):
    enlace = (url_for('recuperar', token = token, _external = True))
    msg = Message('Test password', sender= config('USER_MAIL'),
                recipients= [mailing])

    msg.html = render_template('email.html', name = name)
    msg.html+= f'<p> <a herf = "{enlace}">{enlace}</a></p>'

    mail.send(msg)

