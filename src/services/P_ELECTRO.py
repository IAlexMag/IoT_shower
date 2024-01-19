from gpiozero import DigitalOutputDevice
import time

# Configura el pin de la electroválvula (ajústalo al pin que estás utilizando)
pin_electrovalvula = 21
#electrovalvula = DigitalOutputDevice(pin_electrovalvula,active_high=False)
electrovalvula = DigitalOutputDevice(pin_electrovalvula)

def encender_electrovalvula():
    electrovalvula.on()
    print("Electroválvula encendida")

def apagar_electrovalvula():
    electrovalvula.off()
    print("Electroválvula apagada")

def main():
    encender_electrovalvula()

    try:
        # Espera 30 segundos
        time.sleep(1)
    finally:
        apagar_electrovalvula()

if __name__ == "__main__":
    main()
