# -*- coding:UTF-8 -*-
import serial  
import time  
# 打开串口  
ser = serial.Serial("/dev/ttyAMA0", 9600)  
def main():         
    while True:
        ser.write(b'Raspberry pi')
        time.sleep(1)
