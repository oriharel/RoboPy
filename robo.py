# import RPi.GPIO as GPIO
import gtts
import pygame
from flask import Flask
from flask import request
from adafruit_motorkit import MotorKit
import os
# import wiringpi
# import sys

kit = MotorKit()


# speed = 0.4
# reveres_speed = -0.4
# GPIO.setwarnings(False)    # Ignore warning for now
# GPIO.setmode(GPIO.BCM)   # Use physical pin numbering
# GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)   # Set pin 4 to be an output pin and set initial

# wiringpi.wiringPiSetupGpio()
# wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
# wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# wiringpi.pwmSetClock(192)
# wiringpi.pwmSetRange(2000)
# wiringpi.pwmWrite(18, 75)


# def signal_handler(sig, frame):
#     print('You pressed Ctrl+C!')
#     GPIO.cleanup()
#     sys.exit(0)
#
#
# def set_interval(func, sec):
#     def func_wrapper():
#         set_interval(func, sec)
#         func()
#
#     t = threading.Timer(sec, func_wrapper)
#     t.start()
#     return t


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

# def set_light():
#     channel_is_on = GPIO.input(4)
#     print('channel_is_on is {}'.format(channel_is_on))
#     if channel_is_on:
#         GPIO.output(4, GPIO.LOW)
#     else:
#         GPIO.output(4, GPIO.HIGH)

# def set_camera(ms):
#     wiringpi.pwmWrite(18, ms)
#
# def set_cameraUp():
#     wiringpi.pwmWrite(18, 250)
#
# def set_cameraDown():
#     wiringpi.pwmWrite(18, 40)
#
# def set_cameraCenter():
#     wiringpi.pwmWrite(18, 150)


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

# @app.route('/light')
# def light():
#     set_light()
#     return 'Hello light'
#
# @app.route('/cameraUp')
# def cameraUp():
#     set_cameraUp()
#     return 'Hello set_cameraUp'
#
# @app.route('/cameraDown')
# def cameraDown():
#     set_cameraDown()
#     return 'Hello set_cameraDown'
#
# @app.route('/cameraCenter')
# def cameraCenter():
#     set_cameraCenter()
#     return 'Hello set_cameraCenter'\

# @app.route('/cameraSet/<int:ms>')
# def cameraSet(ms):
#     set_camera(ms)
#     return 'Hello set_camera'

@app.route('/speak', methods=['POST'])
def speak():
    req_data = request.get_json()
    text = req_data['text']
    tts = gtts.gTTS(text)
    os.remove("text.mp3")
    tts.save("text.mp3")
    pygame.mixer.init()
    pygame.mixer.music.load("text.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    return 'Hello speak'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
