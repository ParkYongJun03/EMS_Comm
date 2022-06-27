import RPi.GPIO as GPIO
import time

RED = 11
GREEN = 12
BLUE = 13

GPIO.setmode(GPIO.BOARD) # GOIO.BCM
GPIO.setup(RED, GPIO.OUT) # 11핀 출력 세팅
GPIO.setup(GREEN, GPIO.OUT) # 12핀 출력 세팅
GPIO.setup(BLUE, GPIO.OUT) # 13핀 출력 세팅
# GH=GPIO.HIGH
# GL=GPIO.LOW
cnt = 0
try : 
    while True :
        cnt = cnt%3+1
        GPIO.output(RED, cnt==1)
        GPIO.output(GREEN, cnt==2)
        GPIO.output(BLUE, cnt==3)
        time.sleep(1.0)
except KeyboardInterrupt:
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(BLUE, GPIO.LOW)