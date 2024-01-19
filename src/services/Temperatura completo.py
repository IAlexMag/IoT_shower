import time
import board
import busio
import adafruit_tca9548a
import adafruit_mlx90614
import Adafruit_DHT
from Adafruit_DHT import DHT11 as AdafruitDHT11

# Configuración de los pines
dht_pin = 17  # Cambia esto al pin GPIO donde está conectado tu sensor DHT11

# Configuración de los buses I2C
i2c_bus = busio.I2C(board.SCL, board.SDA)

# Conectar el multiplexor
tca = adafruit_tca9548a.TCA9548A(i2c_bus, address=0x70)

# Conectar el sensor GY-906 #1 al canal 0 del multiplexor
mlx90614_1 = adafruit_mlx90614.MLX90614(tca[0])

# Conectar el sensor GY-906 #2 al canal 1 del multiplexor
mlx90614_2 = adafruit_mlx90614.MLX90614(tca[2])

# Configurar el tipo de sensor DHT11 y el pin
sensor_dht = Adafruit_DHT.DHT11

try:
    while True:
       
        # Medir la temperatura del tubo 1 con GY-906 #1
        temp_tubo_1 = mlx90614_1.object_temperature
        print(f'Temperatura del tubo 1: {temp_tubo_1:.2f} °C')

        # Medir la temperatura del tubo 2 con GY-906 #2
        temp_tubo_2 = mlx90614_2.object_temperature
        print(f'Temperatura del tubo 2: {temp_tubo_2:.2f} °C')

        # Medir la temperatura del ambiente con DHT11
        humidity, temperature_ambiente = Adafruit_DHT.read_retry(sensor_dht, dht_pin)
        print(f'Temperatura del ambiente: {temperature_ambiente:.2f} °C, Humedad: {humidity:.2f}%')

        time.sleep(.1)  # Espera 2 segundos antes de la siguiente medición

except KeyboardInterrupt:
    pass
