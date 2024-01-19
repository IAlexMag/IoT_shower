from gpiozero import DigitalOutputDevice
from time import sleep

# Definición de pines para las electroválvulas
valvula_agua_fria_pin = 21  # Reemplaza con el pin GPIO correcto
valvula_agua_caliente_pin = 20  # Reemplaza con el pin GPIO correcto

# Configuración de electroválvulas
valvula_agua_fria = DigitalOutputDevice(valvula_agua_fria_pin)
valvula_agua_caliente = DigitalOutputDevice(valvula_agua_caliente_pin, active_high=False)

def encender_valvula(valvula):
    valvula.on()

def apagar_valvula(valvula):
    valvula.off()

def main():
    try:
        while True:
            # Obtener el tiempo de encendido desde la consola
            tiempo_encendido = int(input("Ingrese el tiempo de encendido en segundos: "))

            # Encender electroválvulas
            tipo_valvula = input("Ingrese el tipo de electroválvula (fria/caliente): ")

            if tipo_valvula == "fria":
                encender_valvula(valvula_agua_fria)
                sleep(tiempo_encendido)
                apagar_valvula(valvula_agua_fria)
            elif tipo_valvula == "caliente":
                encender_valvula(valvula_agua_caliente)
                sleep(tiempo_encendido)
                apagar_valvula(valvula_agua_caliente)

    except KeyboardInterrupt:
        print("Programa detenido manualmente.")

    finally:
        # Apagar todas las electroválvulas antes de salir
        apagar_valvula(valvula_agua_fria)
        apagar_valvula(valvula_agua_caliente)

if __name__ == "__main__":
    main()
