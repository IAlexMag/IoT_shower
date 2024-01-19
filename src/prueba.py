from flask import jsonify, request, Flask
import json

app = Flask(__name__)

datos = [{
    'name': 'Alex',
    'price': 500,
    'description': 'Aleatorio'
}]


def data(datos):
    return print(jsonify(datos))

data(datos)