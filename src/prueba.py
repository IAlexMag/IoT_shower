'''import bcrypt

salt = bcrypt.gensalt()

usuario = {'name': 'aled',
         'lname': 'orenda',
         'mail': 'alexanede@jfjf',
         'password': '12345',
         'gender': 'Male'}
print(usuario)
usuario['password'] = bcrypt.hashpw(usuario.get('password').encode('utf-8'),salt)

print(usuario['password'])

print(usuario)
'''
'''
import requests
from PIL import Image
from time import sleep
while True:
        
    res = requests.get("ipdelacamara/capture")
    #print(res) para obtener el contenido del objeto de respuesta
    with open("archivo,jpg", 'wb') as archivo:
        archivo.write(res.content)

    img = Image.open('archivo.jpg')
    print(img.size)
    sleep(3)
    '''
import flask_mail