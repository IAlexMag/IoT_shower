from gpiozero import DigitalOutputDevice, Button
from time import sleep

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

def medir_flujo(sensor_flujo):
    # Inicia la medición de flujo y muestra el conteo de pulsos
    print("Iniciando medición del flujo. Presiona Enter para detener.")
    sensor_flujo.when_pressed = contar_pulso_fria
    input()
    sensor_flujo.when_pressed = None
    print("Medición del flujo detenida. Pulsos:", cont_pulsos_fria)

def encender_valvula(valvula, tipo_valvula):
    global cont_pulsos_fria, cont_pulsos_caliente
    valvula.on()
    print(f"Encendiendo válvula {tipo_valvula}")
    
    # Restablecer el contador de pulsos antes de cada medición
    cont_pulsos_fria = 0
    cont_pulsos_caliente = 0
    
    # Medir el flujo mientras la válvula está abierta
    medir_flujo(sensor_flujo_fria if tipo_valvula == "fria" else sensor_flujo_caliente)
    
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
