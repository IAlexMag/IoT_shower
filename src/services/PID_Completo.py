from gpiozero import DigitalOutputDevice, Button
from time import sleep, time
from threading import Thread
import board
import busio
import adafruit_tca9548a
import adafruit_mlx90614
import Adafruit_DHT
from Adafruit_DHT import DHT11 as AdafruitDHT11
#from services.bano import params_pid
# Definición de pines para las electroválvulas y sensores de flujo
#data = params_pid()
valvula_agua_fria_pin = 21
valvula_agua_caliente_pin = 20
sensor_flujo_fria_pin = 5
sensor_flujo_caliente_pin = 6
tiempo_final = False
# Configuración de electroválvulas
valvula_agua_fria = DigitalOutputDevice(valvula_agua_fria_pin)
valvula_agua_caliente = DigitalOutputDevice(valvula_agua_caliente_pin, active_high=False)

# Configuración de sensores de flujo
sensor_flujo_fria = Button(sensor_flujo_fria_pin)
sensor_flujo_caliente = Button(sensor_flujo_caliente_pin)

# Configuración de los buses I2C
i2c_bus = busio.I2C(board.SCL, board.SDA)

# Conectar el multiplexor
tca = adafruit_tca9548a.TCA9548A(i2c_bus, address=0x70)

# Conectar el sensor GY-906 para medir la temperatura del tanque
mlx90614_tanque = adafruit_mlx90614.MLX90614(tca[0])
mlx90614_caliente = adafruit_mlx90614.MLX90614(tca[2])
# Configuración del sensor DHT11 para medir la temperatura del agua fría
dht_pin = 17
sensor_dht = Adafruit_DHT.DHT11

# Variables globales para las temperaturas
temperatura_tanque = 0.0
temperatura_fria = 0.0
temperatura_caliente = 0.0

# Funciones para medir la temperatura de los sensores
def medir_temperatura_tanque():
    global temperatura_tanque
    while True:
        temperatura_tanque = mlx90614_tanque.object_temperature
        sleep(.1)  # Ajusta según la frecuencia de actualización deseada

def medir_temperatura_fria():
    global temperatura_fria
    while True:
        humidity, temperatura_fria = Adafruit_DHT.read_retry(sensor_dht, dht_pin)
        sleep(.1)  # Ajusta según la frecuencia de actualización deseada

def medir_temperatura_caliente():
    global temperatura_caliente
    while True:
        temperatura_caliente = mlx90614_caliente.object_temperature
        sleep(.1)  # Ajusta según la frecuencia de actualización deseada

# ... (resto del código)

# Funciones para controlar las electroválvulas
def encender_valvula(valvula, tipo_valvula):
    valvula.on()
    print(f"Encendiendo válvula {tipo_valvula}")

def apagar_valvula(valvula, tipo_valvula):
    valvula.off()
    print(f"Apagando válvula {tipo_valvula}")

# Funciones para medir el flujo de agua
def medir_flujo(sensor_flujo, tipo_valvula, tiempo_funcionamiento):
    print(f"Iniciando medición de flujo para la tubería {tipo_valvula}. Presiona Enter para detener.")
    tiempo_inicio = time()
    pulsos = 0

    while (time() - tiempo_inicio) < tiempo_funcionamiento:
        if sensor_flujo.is_pressed:
            pulsos += 1
            sleep(0.1)  # Ajusta según la respuesta de tu sensor de flujo

    tiempo_fin = time()
    pulsos_por_litro = 400  # Ajusta según tu sensor de flujo
    volumen_litros = pulsos / pulsos_por_litro
    tiempo_encendido = tiempo_fin - tiempo_inicio

    print(f"Medición del flujo detenida. Pulsos: {pulsos}, Volumen: {volumen_litros:.2f} litros, Tiempo encendido: {tiempo_encendido:.2f} segundos")

# Funciones para controlar la temperatura del agua fría y caliente
def controlar_temperatura_fria(setpoint):
    try:
        while True:
            global temperatura_tanque
            print(f'Temperatura Tanque: {temperatura_tanque:.2f} °C')
            print("Temperatura Fria:", temperatura_fria, "°C")

            if temperatura_tanque > setpoint:
                encender_valvula(valvula_agua_fria, "fria")
            else:
                apagar_valvula(valvula_agua_fria, "fria")

            sleep(0.1)

    except KeyboardInterrupt:
        apagar_valvula(valvula_agua_fria, "fria")

def controlar_temperatura_caliente(setpoint):
    try:
        while True:
            global temperatura_tanque
            print(f'Temperatura Tanque: {temperatura_tanque:.2f} °C')
            print("Temperatura Caliente:", temperatura_caliente, "°C")
            if temperatura_tanque < setpoint:
                encender_valvula(valvula_agua_caliente, "caliente")
            else:
                apagar_valvula(valvula_agua_caliente, "caliente")

            sleep(0.1)

    except KeyboardInterrupt:
        apagar_valvula(valvula_agua_caliente, "caliente")

#función para verificar el tiempo corrido
def verifica_tiempo(tiempo_funcionamiento):
    global tiempo_final
    sleep(tiempo_funcionamiento)
    tiempo_final=True

# Función principal del programa
def main(data):
    global tiempo_final
    while True:
        try:
            # Iniciar hilos para medir la temperatura de tanque y caliente
            hilo_temperatura_tanque = Thread(target=medir_temperatura_tanque)
            hilo_temperatura_caliente = Thread(target=medir_temperatura_caliente)
            hilo_temperatura_fria = Thread(target=medir_temperatura_fria)

            hilo_temperatura_tanque.start()
            hilo_temperatura_caliente.start()
            hilo_temperatura_fria.start()

            # Mostrar temperaturas iniciales
            sleep(1)  # Esperar un poco para permitir que los hilos obtengan las primeras mediciones
            print("Temperatura Inicial Tanque:", temperatura_tanque, "°C")
            print("Temperatura Inicial Caliente:", temperatura_caliente, "°C")
            print("Temperatura Inicial Fria:", temperatura_fria, "°C")

            # Ingresar el set point de temperatura y tiempo de funcionamiento
            setpoint = float(data.get("temperature",0))
            #setpoint = float(input("Ingrese el set point de temperatura: "))
            tiempo_funcionamiento = int(data.get("duracion",0))*60
            #tiempo_funcionamiento = int(input("Ingrese el tiempo de funcionamiento en minutos: ")) * 60
            hilo_verifica_tiempo = Thread(target=verifica_tiempo, args=(tiempo_funcionamiento,))
            hilo_verifica_tiempo.start()

            # Iniciar hilos para controlar la temperatura y medir el flujo
            hilo_control_fria = Thread(target=controlar_temperatura_fria, args=(setpoint,))
            hilo_control_caliente = Thread(target=controlar_temperatura_caliente, args=(setpoint,))
            hilo_medir_flujo_fria = Thread(target=medir_flujo, args=(sensor_flujo_fria, "fria", tiempo_funcionamiento))
            hilo_medir_flujo_caliente = Thread(target=medir_flujo, args=(sensor_flujo_caliente, "caliente", tiempo_funcionamiento))

            # Iniciar los hilos
            hilo_control_fria.start()
            hilo_control_caliente.start()
            hilo_medir_flujo_fria.start()
            hilo_medir_flujo_caliente.start()

            # Esperar a que los hilos terminen
            hilo_control_fria.join()
            hilo_control_caliente.join()
            hilo_medir_flujo_fria.join()
            hilo_medir_flujo_caliente.join()

        except KeyboardInterrupt:
            pass

        finally:
            # Apagar todas las electroválvulas antes de salir
            if tiempo_final:    
                valvula_agua_fria.off()
                valvula_agua_caliente.off()
                tiempo_final = False

if __name__ == "__main__":
    pass
