## PUSH BUTTON TGB LED Control 2
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

GPIO.setup(BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

isClick= False
count = 0

def button_push(channel) : 
    global count
    print("Button Pushed ! ")
    count += 1
    if (count % 5 == 1) : #RED
        GPIO.output(RED, 1)
        GPIO.output(GREEN, 0)
        GPIO.output(BLUE, 0)
    elif (count % 5 == 2) : #GREEN
        GPIO.output(RED, 0)
        GPIO.output(GREEN, 1)
        GPIO.output(BLUE, 0)
    elif (count % 5 == 3) : #BLUE
        GPIO.output(RED, 0)
        GPIO.output(GREEN, 0)
        GPIO.output(BLUE, 1)
    elif (count % 5 == 4) : #WHITE
        GPIO.output(RED, 1)
        GPIO.output(GREEN, 1)
        GPIO.output(BLUE, 1)
    elif (count % 5 == 0) : #NOTHING
        GPIO.output(RED, 0)
        GPIO.output(GREEN, 0)
        GPIO.output(BLUE, 0)


GPIO.add_event_detect(BUTTON, GPIO.RISING, 
                callback=button_push, bouncetime=100)   


try : 
    while True :
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.LOW)