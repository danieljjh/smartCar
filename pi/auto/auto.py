# -*- coding:UTF-8 -*-
import time
import datetime
from car import *
from camera import *


def main():
    GPIO.setup(start_btn,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.setup(cam_btn,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    for x in range(5):
        while True:
            if sum(car.ir()) > 1:
                car.forward()
            else:
                car.brake()
                car.backward()
                time.sleep(1)
            time.sleep(0.02)


if __name__ == '__main__':

    GPIO.setup(start_btn,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(cam_btn,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.setup(cam_btn,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #     
    car = Car()

    while 1:
        # start = GPIO.wait_for_edge(start_btn, GPIO.RISING)
        # GPIO.setup(23, GPIOIN, pull_up_down=GPIO.PUD_UP)
        Input_state = GPIO.input(start_btn)
        set = True
        if Input_state  and set :
            time.sleep(2)
            main()
        else:
            break