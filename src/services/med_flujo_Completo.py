from gpiozero import DigitalOutputDevice, Button
from time import sleep, time

# Definición de pines para las electroválvulas y sensores de flujo
valvula_agua_fria_pin = 21  # Reemplaza con el pin GPIO correcto
valvula_agua_caliente_pin = 20  # Reemplaza con el pin GPIO correcto
sensor_flujo_fria_pin = 5  # Reemplaza con el pin GPIO correcto
sensor_flujo_caliente_pin = 6  # Reemplaza con el pin GPIO correcto

# Configuración de electroválvulas
valvula_agua_fria = DigitalOutputDevice(valvula_agua_fria_pin)
valvula_agua_caliente = DigitalOutputDevice(valvula_agua_caliente_pin, active_high=False)

# Configuración de sensores de flujo
sensor_flujo_fria = Button(sensor_flujo_fria_pin)
sensor_flujo_caliente = Button(sensor_flujo_caliente_pin)

# Inicialización de los contadores de pulsos para el flujo frío y caliente
cont_pulsos_fria = 0
cont_pulsos_caliente = 0

# Pulsos por litro (reemplaza con los valores específicos de tu sensor)
pulsos_por_litro_fria = 400
pulsos_por_litro_caliente = 390

# Funciones para contar pulsos de los sensores de flujo
def contar_pulso_fria():
    global cont_pulsos_fria
    cont_pulsos_fria += 1

def contar_pulso_caliente():
    global cont_pulsos_caliente
    cont_pulsos_caliente += 1

# Asignación de las funciones de conteo a los eventos de pulsación
sensor_flujo_fria.when_pressed = contar_pulso_fria
sensor_flujo_caliente.when_pressed = contar_pulso_caliente

def medir_flujo(sensor_flujo, tipo_valvula):
    # Inicia la medición de flujo y muestra el conteo de pulsos
    print("Iniciando medición del flujo. Presiona Enter para detener.")
    tiempo_inicio = time()
    sensor_flujo.when_pressed = contar_pulso_fria if tipo_valvula == "fria" else contar_pulso_caliente
    input()
    sensor_flujo.when_pressed = None
    tiempo_fin = time()

    # Calcula el volumen en litros
    pulsos = cont_pulsos_fria if tipo_valvula == "fria" else cont_pulsos_caliente
    pulsos_por_litro = pulsos_por_litro_fria if tipo_valvula == "fria" else pulsos_por_litro_caliente
    volumen_litros = pulsos / pulsos_por_litro

    # Calcula el tiempo que la válvula estuvo abierta
    tiempo_encendido = tiempo_fin - tiempo_inicio

    print(f"Medición del flujo detenida. Pulsos: {pulsos}, Volumen: {volumen_litros:.2f} litros, Tiempo encendido: {tiempo_encendido:.2f} segundos")

def encender_valvula(valvula, tipo_valvula):
    global cont_pulsos_fria, cont_pulsos_caliente
    valvula.on()
    print(f"Encendiendo válvula {tipo_valvula}")

    # Restablecer el contador de pulsos antes de cada medición
    cont_pulsos_fria = 0
    cont_pulsos_caliente = 0

    # Medir el flujo mientras la válvula está abierta
    medir_flujo(sensor_flujo_fria if tipo_valvula == "fria" else sensor_flujo_caliente, tipo_valvula)

    # Detener la medición y apagar la válvula
    valvula.off()
    print(f"Apagando válvula {tipo_valvula}")

def main():
    try:
        while True:
            # Encender electroválvulas y medir el flujo
            tipo_valvula = input("Ingrese el tipo de electroválvula (fria/caliente): ")

            if tipo_valvula == "fria":
                encender_valvula(valvula_agua_fria, tipo_valvula)
            elif tipo_valvula == "caliente":
                encender_valvula(valvula_agua_caliente, tipo_valvula)
            else:
                print("Tipo de válvula no reconocido. Use 'fria' o 'caliente'.")

    except KeyboardInterrupt:
        print("Programa detenido manualmente.")

    finally:
        # Apagar todas las electroválvulas antes de salir
        valvula_agua_fria.off()
        valvula_agua_caliente.off()

if __name__ == "__main__":
    main()
