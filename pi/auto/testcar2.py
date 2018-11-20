# -*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import string
import serial

'''
int E1 = 5; // PWM A
int M1 = 4; // DIR A
int E2 = 6; // PWM B
int M2 = 7; // DIR B

int Val = 0 ;
int ChangeValue = 20;
void setup()
{
pinMode(M1, OUTPUT);
pinMode(M2, OUTPUT);
}

void forward()
{
  digitalWrite(M1, LOW);
  digitalWrite(E1, Val);
  
  digitalWrite(M2, LOW);
  digitalWrite(E2, Val);

}


'''
# 小车电机引脚定义
# 使用 L298P 时 
# PWMA : 5 
# ENA 16 ->PWMA 5
# ENB  13-> PWMB 6
# DIRA :4
# IN1 20 ->DIRA 4
# DIRB :7 
# IN3 19-> DRIB 7

IN1 = 20
IN3 = 19

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

CarSpeedControl = 50
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#: motor
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)

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


def forward(t):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)
    time.sleep(t)


def turn_right(t):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)
    time.sleep(t)


def turn_left(t):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)
    time.sleep(t)


def brake():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)


def backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)


if __name__ == '__main__':

    while 1:
        forward()
        time.sleep(2)
        backward()
        time.sleep(2)
