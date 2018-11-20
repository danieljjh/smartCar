from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import math
import RPi.GPIO as GPIO
import io

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(7, GPIO.OUT)
# GPIO.setup(8, GPIO.OUT)
theta = 0
minLineLength = 5
maxLineGap = 20
camera = PiCamera()
camera.resolution = (240, 160)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(240, 160))
time.sleep(1)
i = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    i = i + 1
 #    print(i)
    imgr = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    #     plt.imshow(imgr)
    #     plt.show()
    minRGB = np.array([15, 0, 0])
    maxRGB = np.array([38, 255, 255])
    y_mask = cv2.inRange(imgr, minRGB, maxRGB)
    masks = cv2.bitwise_or(imgr, imgr, mask=y_mask)
    plt.imshow(y_mask)
    plt.show()
    gray = cv2.cvtColor(masks, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 250, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 3, np.pi/180, 20, 10, 5)
    if lines is None:
        pass
    else:
        for x in range(0, len(lines)):
            for x1, y1, x2, y2 in lines[x]:
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                theta = round(theta+math.atan2((y2-y1), (x2-x1)), 3)
                slope = round((y2 - y1) / (x2 - x1), 3)
                print('line  theta %2f slope: %2f' % (theta, slope))
        cv2.imwrite("imgs/line" + str(i) + " theta-" +
                    str(theta) + " slope- " + str(slope) + ".png", image)
    rawCapture.truncate(0)
