# -*- coding:UTF-8 -*-
import cv2
import numpy as np
import sys
import picamera
from picamera.array import PiRGBArray
import io
import math

import RPi.GPIO as GPIO
import time

# GPIO.cleanup()
#: 马达端口
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26

# ENA = 6
# ENB = 5
ENA = 16  # 右
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

Speed = 50
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
# GPIO.setup(EchoPin, GPIO.IN)
# GPIO.setup(TrigPin, GPIO.OUT)

#: led
GPIO.setup(LED_R, GPIO.OUT)
GPIO.setup(LED_G, GPIO.OUT)
GPIO.setup(LED_B, GPIO.OUT)

#: Ir
# GPIO.setup(AvoidSensorLeft, GPIO.IN)
# GPIO.setup(AvoidSensorRight, GPIO.IN)

#: led
pwm_rled = GPIO.PWM(LED_R, 1000)
pwm_gled = GPIO.PWM(LED_G, 1000)
pwm_bled = GPIO.PWM(LED_B, 1000)
pwm_rled.start(0)
pwm_gled.start(0)
pwm_bled.start(0)

print('initialized..')
def forward(t):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(Speed)
    pwm_ENB.ChangeDutyCycle(Speed)
    time.sleep(t)
    brake()
#     GPIO.output(IN1, GPIO.LOW)
#     GPIO.output(IN2, GPIO.LOW)
#     GPIO.output(IN3, GPIO.LOW)
#     GPIO.output(IN4, GPIO.LOW)
#     pwm_ENA.ChangeDutyCycle(0)
#     pwm_ENB.ChangeDutyCycle(0)


def turn_right(t):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(Speed)
    pwm_ENB.ChangeDutyCycle(Speed)
    pwm_bled.ChangeDutyCycle(50)
    time.sleep(t)
    brake()
    pwm_bled.ChangeDutyCycle(0)


def turn_left(t):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(Speed)
    pwm_ENB.ChangeDutyCycle(Speed)
    pwm_rled.ChangeDutyCycle(50)
    time.sleep(t)
    brake()
    pwm_rled.ChangeDutyCycle(0)
    
#     time.sleep(t)


def brake():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(0)
    pwm_ENB.ChangeDutyCycle(0)


def backward(t):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(Speed)
    pwm_ENB.ChangeDutyCycle(Speed)
    time.sleep(t)
    brake()


def servo_control_color():
    for pos in range(181):
        pwm_servo.ChangeDutyCycle(2.5 + 10 * pos/180)
        time.sleep(0.009)
    for pos in reversed(range(181)):
        pwm_servo.ChangeDutyCycle(2.5 + 10 * pos/180)
        time.sleep(0.009)


def yewllow_circle():
    print('start...')
    with picamera.PiCamera() as camera:
        camera.resolution = (240, 160)
        camera.framerate = 10
        time.sleep(2)
        start = time.time()
        i = 0
        rawCapture = PiRGBArray(camera, size=(240, 160))
        for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
            image = frame.array
#             plt.imshow(image)
#             plt.show()
            i = i + 1
#             image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # img3 = image[:,:,[0,0,1]]
            # image = cv2.blur(image,(5,5))
            h = image.shape
            img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

            redMin = np.array([12, 100, 100])
            redMax = np.array([27, 255, 255])
            red_m = cv2.inRange(img_hsv, redMin, redMax)
            r_mask = cv2.bitwise_or(img_hsv, img_hsv, mask=red_m)
            gray = cv2.cvtColor(r_mask, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 250, apertureSize=3)

            dp = 1
            c1 = 30
            c2 = 12
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp, 30, param1=c1, param2=c2, minRadius=25, maxRadius=40)
#             print('circles ', circles)
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    # draw the outer circle
#                     print(np.array([int(image.shape[0]/2), int(image.shape[1]/2)]))
                    d =  i[0] - 120
                    print('object to center  ', d, i[0])
                    if d < 0:
                        # print('left..')
                        turn_left(.5)
                    else:
                        # print('right..')
                        turn_right(.5)
                    cv2.circle(image, (i[0], i[1]), i[2], (10, 220, 250), 2)
                    # draw the center of the circle
                    cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 2)
#                 cv2.imwrite("imgs/yellow" + str(i) + ".png", image)
                # plt.imshow(image)
                # plt.show()
#                 return i[0], i[1]
            rawCapture.truncate(0)

if __name__ == '__main__':
    yewllow_circle()