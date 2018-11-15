# -*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import string
import serial


# 小车电机引脚定义
# 使用 L298P 时  ENA 16 ->PWMA ENB  13-> PWMB
# IN1 20 ->DIRA IN3 19-> DRIB 

IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26

ENA = 16
ENB = 13

# 超声波引脚定义
EchoPin = 0
TrigPin = 1

# RGB三色灯引脚定义
LED_R = 22
LED_G = 27
LED_B = 24

# 红外避障引脚定义
AvoidSensorLeft = 12
AvoidSensorRight = 17

# 蜂鸣器引脚定义
buzzer = 8

#: button
start_btn = 18
cam_btn = 4

CarSpeedControl = 20
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#: motor
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

# 设置pwm引脚和频率为2000hz
pwm_ENA = GPIO.PWM(ENA, 2000)
pwm_ENB = GPIO.PWM(ENB, 2000)
pwm_ENA.start(0)
pwm_ENB.start(0)

#: ultra
GPIO.setup(EchoPin, GPIO.IN)
GPIO.setup(TrigPin, GPIO.OUT)

#: led
GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
GPIO.setup(LED_B, GPIO.OUT)

#: Ir
GPIO.setup(AvoidSensorLeft, GPIO.IN)
GPIO.setup(AvoidSensorRight, GPIO.IN)

#: led
pwm_rled = GPIO.PWM(LED_R, 1000)
pwm_gled = GPIO.PWM(LED_G, 1000)
pwm_bled = GPIO.PWM(LED_B, 1000)
pwm_rled.start(0)
pwm_gled.start(0)
pwm_bled.start(0)

class Car(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)


        GPIO.setup(start_btn,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(cam_btn,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # #: motor
        # GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
        # GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
        # GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
        # GPIO.setup(ENB, GPIO.OUT, initial=GPIO.HIGH)
        # GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
        # GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

        # # 设置pwm引脚和频率为2000hz
        # pwm_ENA = GPIO.PWM(ENA, 2000)
        # pwm_ENB = GPIO.PWM(ENB, 2000)
        # pwm_ENA.start(0)
        # pwm_ENB.start(0)

        # #: ultra
        # GPIO.setup(EchoPin, GPIO.IN)
        # GPIO.setup(TrigPin, GPIO.OUT)

        # #: led
        # GPIO.setup(LED_R, GPIO.OUT)
        # GPIO.setup(LED_G, GPIO.OUT)
        # GPIO.setup(LED_B, GPIO.OUT)

        # #: Ir
        # GPIO.setup(AvoidSensorLeft, GPIO.IN)
        # GPIO.setup(AvoidSensorRight, GPIO.IN)

        # #: led
        # pwm_rled = GPIO.PWM(LED_R, 1000)
        # pwm_gled = GPIO.PWM(LED_G, 1000)
        # pwm_bled = GPIO.PWM(LED_B, 1000)
        # pwm_rled.start(0)
        # pwm_gled.start(0)
        # pwm_bled.start(0)

    def forward(self):
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENA.ChangeDutyCycle(CarSpeedControl)
        pwm_ENB.ChangeDutyCycle(CarSpeedControl)

    def turn_right(self):
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENA.ChangeDutyCycle(CarSpeedControl)
        pwm_ENB.ChangeDutyCycle(CarSpeedControl)

    def turn_left(self):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.HIGH)
        GPIO.output(IN4, GPIO.LOW)
        pwm_ENA.ChangeDutyCycle(CarSpeedControl)
        pwm_ENB.ChangeDutyCycle(CarSpeedControl)

    def brake(self):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.LOW)

    def backward(self):
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        pwm_ENA.ChangeDutyCycle(CarSpeedControl)
        pwm_ENB.ChangeDutyCycle(CarSpeedControl)

    def distance(self):
        GPIO.output(TrigPin, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(TrigPin, GPIO.LOW)
        while not GPIO.input(EchoPin):
            pass
            t1 = time.time()
        while GPIO.input(EchoPin):
            pass
            t2 = time.time()
        print("distance is %d " % (((t2 - t1) * 340 / 2) * 100))
        time.sleep(0.02)
        return ((t2 - t1) * 340 / 2) * 100

    def ir(self):
        LeftValue = GPIO.input(AvoidSensorLeft)
        RightValue = GPIO.input(AvoidSensorRight)
        return [LeftValue, RightValue]

        

def start_btn():
    