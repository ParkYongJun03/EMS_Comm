#Servo Motor test
import RPi.GPIO as GPIO
import time

#SB = 22
SB = 15

GPIO.setmode(GPIO.BOARD) # GPIO.BOARD
# GPIO.setmode(GPIO.BCM) # GPIO.BCM
GPIO.setup(SB, GPIO.OUT) # 15핀 할당

pwm = GPIO.PWM(SB, 50) # 50Hz
pwm.start(3.0) # 0.6ms

for cnt in range(0,3) :
    pwm.ChangeDutyCycle(3.0)    #0도 회전
    time.sleep(0.5)             #0.5초
    pwm.ChangeDutyCycle(7.5)    #90도 회전
    time.sleep(0.5)             #0.5초
    pwm.ChangeDutyCycle(12.5)   #180도 회전
    time.sleep(0.5)             #0.5초
pwm.ChangeDutyCycle(3.0)    #0도 회전
time.sleep(0.5)             #0.5초


pwm.stop()
GPIO.cleanup()