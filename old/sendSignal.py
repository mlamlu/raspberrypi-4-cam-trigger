import RPi.GPIO as GPIO
import time

PIN_SEND = 37
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_SEND, GPIO.OUT)

try:
    while True:
        print("send signal...")
        GPIO.output(PIN_SEND, GPIO.HIGH)  # Envoyer le signal en niveau haut
        time.sleep(1)  # Attendre pendant 0.5 seconde
        GPIO.output(PIN_SEND, GPIO.LOW)   # Envoyer le signal en niveau bas
        time.sleep(10)  # Attendre pendant 4.5 secondes (total 5 secondes)

except KeyboardInterrupt:
    GPIO.cleanup()  # Nettoyage des configurations GPIO en cas d'interruption
