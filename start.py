# Pas de bug au demarrage mais prend trop de photo
import RPi.GPIO as gp
import os
import time
from time import sleep   # Gestion du temps
from datetime import datetime
from env import raspberry_picture_path


gp.setmode(gp.BOARD)
gp.setup(37, gp.OUT) # Creation sorti 3v
gp.setup(36, gp.IN)  # Une entree : le poussoir
gp.output(37, gp.HIGH)

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
gp.add_event_detect(36, gp.FALLING, callback=my_callback, bouncetime=1000)
print("Maintenant, le programme surveille les actions sur le poussoir\n")
run = True
while (run) : #boucle jusqu'a interruption
    try:
        sleep(30)
        print("LOOP")
        
    except KeyboardInterrupt:
        print("\nInterruption par clavier.")
        run = False
        
print("CLEAN")
