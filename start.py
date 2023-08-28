import RPi.GPIO as GPIO
import os
import time
from datetime import datetime
from env import raspberry_picture_path
import threading
from captureCam import captureAll, close

PIN_RECEIVE = 36

def detect_signal(channel):
    if GPIO.input(PIN_RECEIVE) == GPIO.HIGH:
        print("Signal détecté!")
        camManager.generateThread()

class CaptureManager:
    def __init__(self):
        self.thread = None
    def generateThread(self):
        if self.thread is None or not self.thread.is_alive():
            thread = threading.Thread(target=captureAll)
            thread.start()
            print("Thread arduCam démarré")
            thread.join()
            print("Thread join")
        else:
            print("Thread de la Fonction B est déjà en cours d'exécution")


GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_RECEIVE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

isExist = os.path.exists(raspberry_picture_path)
if not isExist:
    os.mkdir(raspberry_picture_path)

camManager = CaptureManager()
GPIO.add_event_detect(PIN_RECEIVE, GPIO.RISING, callback=detect_signal, bouncetime=75)
print("..Ready to receive signal..")
try:
    while True:
        pass

except KeyboardInterrupt:
    close()
    GPIO.cleanup()  # Nettoyage des configurations GPIO en cas d'interruption


