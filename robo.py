import RPi.GPIO as GPIO
import time
from flask import Flask
import threading
import signal
import sys

def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        GPIO.cleanup()
        sys.exit(0)

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
BLUE_LIGHT = 10
RED_LIGHT = 9
GREEN_LIGHT = 11
MOTION = 22
LEFT_LINE = 27
RIGHT_LINE = 17


GPIO.setup(BLUE_LIGHT,GPIO.OUT)
GPIO.setup(RED_LIGHT,GPIO.OUT)
GPIO.setup(GREEN_LIGHT,GPIO.OUT)
GPIO.setup(MOTION,GPIO.IN)

def blueLightOn():
    GPIO.output(BLUE_LIGHT,GPIO.HIGH)

def blueLightOff():
    GPIO.output(BLUE_LIGHT, GPIO.LOW)

def redLightOn():
    GPIO.output(RED_LIGHT,GPIO.HIGH)

def redLightOff():
    GPIO.output(RED_LIGHT, GPIO.LOW)

def greenLightOn():
    GPIO.output(GREEN_LIGHT,GPIO.HIGH)

def greenLightOff():
    GPIO.output(GREEN_LIGHT, GPIO.LOW)

def toggleBlueLight():
    blueLightOff()
    blueLightOn()
    time.sleep(1)
    blueLightOff()

def allLightsOff():
    blueLightOff()
    redLightOff()
    greenLightOff()

set_interval(toggleBlueLight, 3)

GPIO.add_event_detect(MOTION, GPIO.BOTH, bouncetime=300)

def motionDetected(channel):
    if GPIO.input(channel):
        print "Motion ON Detected!"
        greenLightOn()
        time.sleep(5)
        greenLightOff()

GPIO.add_event_callback(MOTION, motionDetected)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.output(GPIO_TRIGGER, False)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    print ("Measured Distance = %.1f cm" % distance)

set_interval(distance, 1)

app = Flask(__name__)
@app.route('/')
def index():
    return 'Hello world'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')