import Adafruit_DHT
import time

# Configura el tipo de sensor (DHT11)
sensor = Adafruit_DHT.DHT11

# Configura el pin de la Raspberry Pi al que está conectado el sensor
pin = 17

while True:
    # Intenta obtener los datos del sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Verifica si la lectura fue exitosa
    if humidity is not None and temperature is not None:
        # Imprime los resultados
        print(f'Temperatura: {temperature:.2f}°C, Humedad: {humidity:.2f}%')
    else:
        # Imprime un mensaje de error si la lectura falla
        print('Error al leer el sensor DHT11')

    # Espera un tiempo antes de realizar la próxima lectura
    time.sleep(2)
