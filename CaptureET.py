import cv2
from datetime import datetime
import subprocess
import signal
import os
import queue
import RPi.GPIO as GPIO
import time
import threading
from picamera2 import Picamera2, Preview


PIN_RECEIVE = 36
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_RECEIVE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Flag for stopping threads
stop_threads = False
image_queue = queue.Queue(maxsize=100)

Semaphore = threading.Semaphore(1)

# Lock for thread synchronization
lock = threading.Lock()

# Function for handling keyboard interrupt signal
def signal_handler(sig, frame):
    global stop_threads
    stop_threads = True
    os._exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Class for controlling the camera
class CameraModule():
    picam2 = None

    def run(self):
        # Initialize the Picamera2 object
        global picam2
        picam2 = Picamera2()
        # Disable preview to save resources
        picam2.start_preview(Preview.NULL)
        # Create a still configuration and configure the camera
        capture_config = picam2.create_still_configuration()
        picam2.configure(capture_config)
        # Start the camera
        picam2.start()
        time.sleep(1)

        # Keep capturing images and add them to the queue
        #while True:
        #    image = None
        #    if GPIO.input(PIN_SIGNAL) == GPIO.HIGH:
        #        print("Signal détecté!")
        #        try:
        #            #image = picam2.capture_array("main")
        #            if image is not None:
        #                image_queue.put(image)
        #                print("Add image to queue.")
        #                Semaphore.release()
        #        except Exception as e:
        #           print(e)
    
    def detect_signal(chan1, chan2):
        global camera
        if GPIO.input(PIN_RECEIVE) == GPIO.HIGH:
            print("Signal détecté!")
            try:
                image = picam2.capture_array("main")
                if image is not None:
                    image_queue.put(image)
                    print("Add image to queue.")
                    Semaphore.release()
            except Exception as e:
               print(e)

class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.camera_module = CameraModule()

    def run(self):
        if self.threadID == 1:
            self.camera_module.run()
            GPIO.add_event_detect(PIN_RECEIVE, GPIO.RISING, callback=self.camera_module.detect_signal, bouncetime=500)

# Thread for saving images
class SaveImageThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        while not stop_threads:
            Semaphore.acquire()
            if not image_queue.empty():
                image = image_queue.get()
                cv2.imwrite("{}.jpg".format(datetime.now()), cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

if __name__ == '__main__':
    # Create and start the threads
    thread1 = SaveImageThread()
    thread1.start()
    thread2 = myThread(1, "Thread-Camera")
    thread2.start()
    # Wait for the threads to complete
    thread2.join()
