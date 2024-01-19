from gpiozero import DigitalOutputDevice, Button
from time import sleep, time
import board
import busio
import adafruit_tca9548a
import adafruit_mlx90614
import Adafruit_DHT

# Configuración de los pines
valvula_agua_fria_pin = 21  # Reemplaza con el pin GPIO correcto
valvula_agua_caliente_pin = 20  # Reemplaza con el pin GPIO correcto
sensor_flujo_salida_pin = 5  # Reemplaza con el pin GPIO correcto
dht_pin = 17  # Reemplaza con el pin GPIO correcto

# Configuración de electroválvulas
valvula_agua_fria = DigitalOutputDevice(valvula_agua_fria_pin)
valvula_agua_caliente = DigitalOutputDevice(valvula_agua_caliente_pin, active_high=False)

# Configuración de sensores
i2c_bus = busio.I2C(board.SCL, board.SDA)
tca = adafruit_tca9548a.TCA9548A(i2c_bus, address=0x70)
sensor_flujo_salida = Button(sensor_flujo_salida_pin)
sensor_temperatura_fria = Adafruit_DHT.DHT11
sensor_temperatura_caliente = adafruit_mlx90614.MLX90614(tca[2])

# Inicialización de los contadores de pulsos para el flujo de salida
cont_pulsos_salida = 0

# Pulsos por litro (ajusta según tus necesidades)
pulsos_por_litro_salida = 100

# Funciones para contar pulsos de los sensores de flujo
def contar_pulso_salida():
    global cont_pulsos_salida
    cont_pulsos_salida += 1

# Asignación de las funciones de conteo a los eventos de pulsación
sensor_flujo_salida.when_pressed = contar_pulso_salida

# Función para medir el flujo de salida
def medir_flujo_salida():
    global cont_pulsos_salida
    print("Iniciando medición del flujo de salida. Presiona Enter para detener.")
    tiempo_inicio = time()
    sensor_flujo_salida.when_pressed = contar_pulso_salida
    input()
    sensor_flujo_salida.when_pressed = None
    tiempo_fin = time()

    pulsos = cont_pulsos_salida
    pulsos_por_litro = pulsos_por_litro_salida
    volumen_litros = pulsos / pulsos_por_litro

    tiempo_encendido = tiempo_fin - tiempo_inicio

    print(f"Medición del flujo de salida detenida. Pulsos: {pulsos}, Volumen: {volumen_litros:.2f} litros, Tiempo encendido: {tiempo_encendido:.2f} segundos")

# Funciones para medir las temperaturas
def medir_temperatura_fria():
    humidity, temperature_ambiente = Adafruit_DHT.read_retry(sensor_temperatura_fria, dht_pin)
    return temperature_ambiente

def medir_temperatura_caliente():
    return sensor_temperatura_caliente.object_temperature

# Función para encender la electroválvula y mantener la temperatura
def mantener_temperatura(setpoint, tiempo_funcionamiento):
    tiempo_inicio = time()
    tiempo_actual = tiempo_inicio
    tiempo_transcurrido = 0

    try:
        while tiempo_transcurrido < tiempo_funcionamiento:
            temperatura_fria = medir_temperatura_fria()
            temperatura_caliente = medir_temperatura_caliente()

            print(f'Temperatura Fria: {temperatura_fria:.2f} °C, Temperatura Caliente: {temperatura_caliente:.2f} °C')

            if temperatura_caliente < setpoint:
                valvula_agua_caliente.on()
            else:
                valvula_agua_caliente.off()

            if temperatura_fria > setpoint:
                valvula_agua_fria.on()
            else:
                valvula_agua_fria.off()

            tiempo_actual = time()
            tiempo_transcurrido = round(tiempo_actual - tiempo_inicio)
            sleep(1)

    finally:
        valvula_agua_fria.off()
        valvula_agua_caliente.off()

if __name__ == "__main__":
    try:
        setpoint = float(input("Ingrese el setpoint de temperatura (entre temperatura fria y caliente): "))
        tiempo_funcionamiento = int(input("Ingrese el tiempo de funcionamiento en segundos: "))

        medir_flujo_salida()
        mantener_temperatura(setpoint, tiempo_funcionamiento)

    except KeyboardInterrupt:
        print("Programa detenido manualmente.")
