from gpiozero import DigitalOutputDevice
from pid_controller import PIDController
from services.temperature import read_temperature
import time

# Crear dos instancias de DigitalOutputDevice para las dos valvulas de agua
valve1 = DigitalOutputDevice(20)
valve2 = DigitalOutputDevice(21)

# Parámetros del controlador PID
kp = 1.0
ki = 0.5
kd = 0.1

# Parámetros de control
target_temperature = 25 # este va a ser el dato que establezca el cliente desde la interfaz web
tolerance = 0.5
control_period = 10 # segundos

# Función para abrir y cerrar las valvulas
def control_valves(open_valve1, open_valve2):
    valve1.value = open_valve1
    valve2.value = open_valve2

# Función para obtener la temperatura actual
def get_current_temperature():
    # Aquí va el código para obtener la temperatura actual del sistema
    # Puedes utilizar, por ejemplo, un sensor de temperatura DHT22 conectado al Raspberry Pi
    temperature = read_temperature()
    return temperature
# Configurar el controlador PID
pid = PIDController(kp, ki, kd)

try:
    while True:
        # Leer la temperatura actual
        current_temperature = get_current_temperature()

        # Calcular la salida del controlador PID
        output = pid.update(target_temperature, current_temperature, control_period)

        # Abre o cierra las valvulas según la salida del controlador PID
        if output > 0:
            control_valves(True, False)
        elif output < 0:
            control_valves(False, True)
        else:
            control_valves(False, False)

        # Verificar si la temperatura actual se encuentra dentro del margen de tolerancia
        if abs(current_temperature - target_temperature) <= tolerance:
            print("Temperatura establecida:", current_temperature)
            break

except KeyboardInterrupt:
    pass