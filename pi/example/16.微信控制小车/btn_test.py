

import RPi.GPIO as GPIO
import time
import string
import serial


# 超声波引脚定义
EchoPin = 0
TrigPin = 1
LED_R = 22
LED_G = 27
LED_B = 24
btn = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
GPIO.setup(LED_B, GPIO.OUT)

# 超声波引脚定义
GPIO.setup(EchoPin, GPIO.IN)
GPIO.setup(TrigPin, GPIO.OUT)
GPIO.setup(btn, GPIO.IN)


pwm_rled = GPIO.PWM(LED_R, 1000)
pwm_gled = GPIO.PWM(LED_G, 1000)
pwm_bled = GPIO.PWM(LED_B, 1000)
pwm_rled.start(0)
pwm_gled.start(0)
pwm_bled.start(0)

pwm_rled.ChangeDutyCycle(0)
GPIO.setup(start_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
while 1:
    if GPIO.input(cam_btn):
        pwm_rled.ChangeDutyCycle(55)
        print(GPIO.input(cam_btn))
        time.sleep(1)
        pwm_rled.ChangeDutyCycle(0)
        GPIO.setup(cam_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


pwm_rled.ChangeDutyCycle(55)
pwm_gled.ChangeDutyCycle(66)
pwm_bled.ChangeDutyCycle(33)


#: 边缘检测


global InputString
global InputStringcache
global StartBit
global NewLineReceived


GPIO.setup(AvoidSensorLeft, GPIO.IN)
GPIO.setup(AvoidSensorRight, GPIO.IN)


def ir():
    LeftValue = GPIO.input(AvoidSensorLeft)
    RightValue = GPIO.input(AvoidSensorRight)
    return [LeftValue, RightValue]


GPIO.setup(start_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(cam_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while 1:
    c = GPIO.wait_for_edge(cam_btn, GPIO.RISING)
    s = GPIO.wait_for_edge(start_btn, GPIO.RISING)
    # c = GPIO.add_event_detect(cam_btn, GPIO.RISING)
    # s = GPIO.add_event_detect(start_btn, GPIO.RISING)
    if c:
        time.sleep(0.01)
        pwm_rled.ChangeDutyCycle(55)
        time.sleep(1)
        print(c)
        print(GPIO.input(cam_btn))
        pwm_rled.ChangeDutyCycle(0)
        GPIO.setup(start_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    if s:
        time.sleep(0.01)
        pwm_gled.ChangeDutyCycle(55)
        pwm_gled.ChangeDutyCycle(0)
        GPIO.setup(start_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        time.sleep(1)
        break


GPIO.setup(start_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(cam_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
while 1:
    c = GPIO.input(cam_btn)
    s = GPIO.input(start_btn)
    if c:
        time.sleep(0.01)
        pwm_rled.ChangeDutyCycle(55)
        time.sleep(1)
        print(c)
        print(GPIO.input(cam_btn))
        pwm_rled.ChangeDutyCycle(0)
    if s:
        time.sleep(0.01)
        pwm_gled.ChangeDutyCycle(55)
        time.sleep(1)
        pwm_gled.ChangeDutyCycle(0)
        break


def forward():
    GPIO.output(IN1, GPIO.HIGH)
    # GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    # print('IN3 %s' % GPIO.output(IN1))
    # GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(50)
    pwm_ENB.ChangeDutyCycle(50)
    time.sleep(10)
    # GPIO.output(IN1, GPIO.LOW)
    # GPIO.output(IN2, GPIO.LOW)
    # GPIO.output(IN3, GPIO.LOW)
    # GPIO.output(IN4, GPIO.LOW)
