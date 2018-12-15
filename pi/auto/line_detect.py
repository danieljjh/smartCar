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


def get_line(image):
    #  img01 = cv2.imread(filename)
    h, w, c = image.shape
#     img01 = cv2.cvtColor(img01, cv2.COLOR_BGR2RGB)
    img01 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)[int(h*1/2):h, :int(w/2), :]
    # plt.imshow(img01)
    # plt.show()
    imgr = cv2.cvtColor(img01, cv2.COLOR_RGB2HSV)
    minRGB = np.array([10, 0, 0])
    maxRGB = np.array([38, 255, 255])
    y_mask = cv2.inRange(imgr, minRGB, maxRGB)
    masks = cv2.bitwise_or(imgr, imgr, mask=y_mask)
    gray = cv2.cvtColor(masks, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 250, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 3, np.pi/180, 20, 5, 5)
    if lines is None:
        return
    y_global_min = img01.shape[0]
    y_max = img01.shape[0]
    l_slope, l_lane = [], []
    for i in range(len(lines)):
        img2 = img01
        line = lines[i]
        x0, y0, x1, y1 = line[0]
        if x1 != x0:
            slope = (y1 - y0)/(x1 - x0)
            if slope < -0.3:
                l_slope.append(slope)
                l_lane.append(line)
    y_global_min = min(y0, y1, y_global_min)
    l_slope_mean = np.mean(l_slope, axis=0)
    l_mean = np.nanmean(np.array(l_lane), axis=0)

    if l_slope_mean == 0 or l_lane is None:
        print('dividing by zero')
        return 1
    l_b = l_mean[0][1] - (l_slope_mean * l_mean[0][0])

    l_x1 = int((y_global_min - l_b)/l_slope_mean)
    l_x2 = int((y_max - l_b)/l_slope_mean)

    l_y1 = y_global_min
    l_y2 = y_max
    cv2.circle(img01, (x0, y0), 5, (255, 0, 0), -11)
    cv2.circle(img01, (x1, y1), 5, (0, 255, 0), -11)
    cv2.line(img01, (x0, y0), (x1, y1), (255, 0, 0), 2)
    cv2.line(img01, (l_x1, l_y1), (l_x2, l_y2), [255, 0, 0], 4)
    return img01


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    i = i + 1
    res = get_line(image)
    plt.imshow(res)
    plt.show()
    rawCapture.truncate(0)
