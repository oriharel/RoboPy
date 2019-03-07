import RPi.GPIO as GPIO
import time
from flask import Flask
from adafruit_motorkit import MotorKit
import threading
import sys

kit = MotorKit()

speed = 0.4
reveres_speed = -0.4

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


def drive_forward():
    kit.motor1.throttle = 1
    kit.motor2.throttle = 1

def drive_backward():
    kit.motor1.throttle = -1
    kit.motor2.throttle = -1

def turn_left():
    kit.motor1.throttle = -1
    kit.motor2.throttle = 1

def turn_right():
    kit.motor1.throttle = 1
    kit.motor2.throttle = -1

def stop_driving():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello world'

@app.route('/forward')
def forward():
    drive_forward()
    return 'Hello forward'

@app.route('/backward')
def backward():
    drive_backward()
    return 'Hello backward'

@app.route('/left')
def left():
    turn_left()
    return 'Hello left'

@app.route('/right')
def right():
    turn_right()
    return 'Hello right'

@app.route('/stop')
def stop():
    stop_driving()
    return 'Hello stop'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
