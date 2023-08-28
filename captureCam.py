from distutils.log import error
import RPi.GPIO as gp
import os
import picamera
from datetime import datetime
from env import host, login, remote_picture_path, raspberry_picture_path

camera = picamera.PiCamera()
camera.resolution = (1920, 1080)

gp.setwarnings(False)
gp.setmode(gp.BOARD)

gp.setup(7, gp.OUT)
gp.setup(11, gp.OUT)
gp.setup(12, gp.OUT)

gp.setup(15, gp.OUT)
gp.setup(16, gp.OUT)
gp.setup(21, gp.OUT)
gp.setup(22, gp.OUT)

gp.output(11, True)
gp.output(12, True)
gp.output(15, True)
gp.output(16, True)
gp.output(21, True)
gp.output(22, True)

def captureAll():
    print("Start testing the camera A")
    i2c = "i2cset -y 1 0x70 0x00 0x04"
    os.system(i2c)
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)
    capture(1)
    print("Start testing the camera B")
    i2c = "i2cset -y 1 0x70 0x00 0x05"
    os.system(i2c)
    gp.output(7, True)
    gp.output(11, False)
    gp.output(12, True)
    capture(2)
    print("Start testing the camera C")
    i2c = "i2cset -y 1 0x70 0x00 0x06"
    os.system(i2c)
    gp.output(7, False)
    gp.output(11, True)
    gp.output(12, False)
    capture(3)
    print("Start testing the camera D")
    i2c = "i2cset -y 1 0x70 0x00 0x07"
    os.system(i2c)
    gp.output(7, True)
    gp.output(11, True)
    gp.output(12, False)
    capture(4)


def capture(cam):
    date_today = datetime.now()
    nom_image = date_today.strftime('%d_%m_%Y_%H:%M:%S.%f')
    path_image = raspberry_picture_path + nom_image + '-CAM'+str(cam)+'.jpg'
    try:
        camera.capture(path_image)
        print("Photo prise")
        command = "scp "+path_image+" "+login+"@"+host+":"+remote_picture_path
        os.system(command)
        print("Photo envoye")
    except error:
        print("Error :", error)

def close():
    gp.output(7, False)
    gp.output(11, False)
    gp.output(12, True)