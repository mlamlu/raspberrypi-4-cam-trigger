import RPi.GPIO as GPIO
import os
import time
from datetime import datetime
from env import raspberry_picture_path

# Numéro des broches GPIO que vous utilisez (numéro de broche physique)
PIN_RECEIVE = 36
PIN_SEND = 37

# Configuration de la bibliothèque RPi.GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_RECEIVE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PIN_SEND, GPIO.OUT)

isExist = os.path.exists(raspberry_picture_path)
if not isExist:
    os.mkdir(raspberry_picture_path)

def detect_signal(channel):
    if GPIO.input(PIN_RECEIVE) == GPIO.HIGH:
        print("Signal détecté!")
        cmd = "python captureCam.py"
        os.system(cmd)

GPIO.add_event_detect(PIN_RECEIVE, GPIO.RISING, callback=detect_signal, bouncetime=75)

try:
    while True:
        print("send signal...")
        GPIO.output(PIN_SEND, GPIO.HIGH)  # Envoyer le signal en niveau haut
        time.sleep(1)  # Attendre pendant 0.5 seconde
        GPIO.output(PIN_SEND, GPIO.LOW)   # Envoyer le signal en niveau bas
        time.sleep(10.5)  # Attendre pendant 4.5 secondes (total 5 secondes)

except KeyboardInterrupt:
    GPIO.cleanup()  # Nettoyage des configurations GPIO en cas d'interruption
