## PUSH BUTTON TGB LED Control 1
import RPi.GPIO as GPIO
import time


BUTTON = 3
RED = 11
GREEN = 12
BLUE = 13

GPIO.setmode(GPIO.BOARD) # GOIO.BCM
GPIO.setup(RED, GPIO.OUT) # 11핀 출력 세팅
GPIO.setup(GREEN, GPIO.OUT) # 12핀 출력 세팅
GPIO.setup(BLUE, GPIO.OUT) # 13핀 출력 세팅

GPIO.setup(BUTTON, GPIO.IN)

isClick= False
# GH=GPIO.HIGH
# GL=GPIO.LOW
def button_push(val) : 
    global isClick 
    if isClick == True:
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.HIGH)
    else:
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)
    isClick = not isClick

try : 
    while True :
        GPIO.wait_for_edge(BUTTON, GPIO.RISING, bouncetime = 100)
        time.sleep(0.1)
        button_push(GPIO.input(BUTTON))
except KeyboardInterrupt:
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.LOW)