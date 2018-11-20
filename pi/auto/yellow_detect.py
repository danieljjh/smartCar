import picamera
from picamera.array import PiRGBArray

import time
import cv2
import numpy as np
import math
import RPi.GPIO as GPIO
# import io

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(7, GPIO.OUT)
# GPIO.setup(8, GPIO.OUT)

# camera = PiCamera()
# camera.resolution = (240, 160)
# camera.framerate = 10
# rawCapture = PiRGBArray(camera, size=(240, 160))
# time.sleep(1)


def yewllow_circle():
    with picamera.PiCamera() as camera:
        camera.resolution = (240, 160)
        camera.framerate = 10
        time.sleep(2)
        start = time.time()
        i = 0
        rawCapture = PiRGBArray(camera, size=(240, 160))
        for frame in camera.capture_continuous(rawCapture, format="rgb", use_video_port=True):
            image = frame.array
            i = i + 1
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # img3 = image[:,:,[0,0,1]]
            # image = cv2.blur(image,(5,5))
            h = image.shape
            img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            # redMin = np.array([130, 40, 50])
            # redMax = np.array([180, 255, 255])
            redMin = np.array([10, 100, 100])
            redMax = np.array([39, 255, 255])
            red_m = cv2.inRange(img_hsv, redMin, redMax)
            r_mask = cv2.bitwise_or(img_hsv, img_hsv, mask=red_m)
            gray = cv2.cvtColor(r_mask, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 250, apertureSize=3)

            dp = 1
            c1 = 30
            c2 = 12
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp, 30,
                                       param1=c1, param2=c2, minRadius=10, maxRadius=20)
            print('circles ', circles)
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    # draw the outer circle
                    print(i)
                    cv2.circle(image, (i[0], i[1]), i[2], (10, 220, 250), 2)
                    # draw the center of the circle
                    cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 2)
                cv2.imwrite("imgs/yellow" + str(i) + ".png", image)
                return 1
            rawCapture.truncate(0)
