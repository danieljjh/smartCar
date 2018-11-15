# -*- coding:UTF-8 -*-
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
# import cv2
import numpy as np
import math
import sys
import os

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 15


def save_image():
    camera.start_preview()
    time.sleep(2)
    filename = str(int(time.time()))
    return camera.capture(filename + '.png')


def save_video():
    fname = str(int(time.time())) + '.h264'
    camera.start_recording(fname)
    camera.wait_recording(10)
    camera.stop_recording()


if __name__ == '__main__':

    save_video()

