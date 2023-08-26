import RPi.GPIO as gp
import os
import time
from time import sleep   # Gestion du temps
from datetime import datetime
from env import raspberry_picture_path

PIN_NUM = 36

gp.setmode(gp.BOARD)
gp.setup(PIN_NUM, gp.IN)  # Une entree : le poussoir

def my_callback(channel):
    if not gp.input(channel):
        print("Input Detected")
        cmd = "python captureCam.py"
        os.system(cmd)


print("Debut du programme")
isExist = os.path.exists(raspberry_picture_path)
if not isExist:
    os.mkdir(raspberry_picture_path)
    
print("Vous pouvez aussi terminer avec CTRL+C \n")
gp.add_event_detect(PIN_NUM, gp.FALLING, callback=my_callback, bouncetime=1000)

try:
    print("Attente de courant électrique...")
    while True:
        pass  # Le programme continue à s'exécuter en arrière-plan

except KeyboardInterrupt:
    gp.cleanup()  # Nettoyage des configurations GPIO en cas d'interruption
