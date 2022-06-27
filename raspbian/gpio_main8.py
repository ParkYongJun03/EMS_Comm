## PUSH BUTTON TGB LED Control 2
import RPi.GPIO as GPIO
import time


BUTTON = 3
RED = 11
GREEN = 12
BLUE = 13
SB = 15

GPIO.setmode(GPIO.BOARD) # GOIO.BOARD
GPIO.setup(RED, GPIO.OUT) # 11핀 출력 세팅
GPIO.setup(GREEN, GPIO.OUT) # 12핀 출력 세팅
GPIO.setup(BLUE, GPIO.OUT) # 13핀 출력 세팅
GPIO.setup(BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

# GPIO.setmode(GPIO.BCM) # GPIO.BCM
GPIO.setup(SB, GPIO.OUT) # 15핀 할당

pwm = GPIO.PWM(SB, 50) # 50Hz
pwm.start(3.0) # 0.6ms

count = 0

def button_push(channel) : 
    global count
    print("Button Pushed ! ")
    count += 1
    if (count % 3 == 1) : #90
        pwm.ChangeDutyCycle(7.5)    #90도 회전
    elif (count % 3 == 2) : #180
        pwm.ChangeDutyCycle(12.5)    #180도 회전
    elif (count % 3 == 0) : #0
        pwm.ChangeDutyCycle(3.0)    #0도 회전

GPIO.add_event_detect(BUTTON, GPIO.RISING, 
                callback=button_push, bouncetime=100)   


try : 
    while True :
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.LOW)