import RPi.GPIO as GPIO
import os
import time
from datetime import datetime
from env import raspberry_picture_path
import threading
from captureCam import capture

PIN_RECEIVE = 36

def detect_signal(channel):
    if GPIO.input(PIN_RECEIVE) == GPIO.HIGH:
        print("Signal détecté!")
        camManager.callArduCam
        print("cmd end")

class CaptureManager:
    def callArduCam(self):
        thread = threading.Thread(target=captureAll)
        thread.start()
        print("Thread callArduCam démarré")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_RECEIVE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

isExist = os.path.exists(raspberry_picture_path)
if not isExist:
    os.mkdir(raspberry_picture_path)

camManager = CaptureManager()
GPIO.add_event_detect(PIN_RECEIVE, GPIO.RISING, callback=detect_signal, bouncetime=75)

try:
    while True:
        pass

except KeyboardInterrupt:
    GPIO.cleanup()  # Nettoyage des configurations GPIO en cas d'interruption


