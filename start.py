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
        print("cmd end")

class CaptureManager:
    def __init__(self):
        self.thread_lock = threading.Lock()  # Verrou pour empêcher le lancement simultané de threads 
    def generateThread(self):
        if not hasattr(self, 'thread') or not self.thread.is_alive():
            print("callArduCam")
            busy = True
            thread = threading.Thread(target=self.captureArduCam)
            thread.start()
            print("Thread arduCam démarré")
        else:
            print("Thread arduCam est déjà en cours d'exécution")
    def captureArduCam(self):
        with self.thread_lock:  # Acquérir le verrou avant d'exécuter la fonction
            captureAll()
            print("Thread arduCam terminé")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_RECEIVE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

isExist = os.path.exists(raspberry_picture_path)
if not isExist:
    os.mkdir(raspberry_picture_path)

camManager = CaptureManager()
GPIO.add_event_detect(PIN_RECEIVE, GPIO.RISING, callback=detect_signal, bouncetime=75)
print("Start program")
try:
    while True:
        pass

except KeyboardInterrupt:
    close()
    GPIO.cleanup()  # Nettoyage des configurations GPIO en cas d'interruption


