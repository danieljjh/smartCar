import RPi.GPIO as GPIO
import time

TrigPin = 4
EchoPin = 3

t1 = 0
t2 = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


GPIO.setup(EchoPin,GPIO.IN)
GPIO.setup(TrigPin,GPIO.OUT)


for i in range(10):
    GPIO.output(TrigPin,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin,GPIO.LOW)
    while not GPIO.input(EchoPin):
        pass
        t1 = time.time()
    while GPIO.input(EchoPin):
        pass
        t2 = time.time()
    print ("distance is %d " % (((t2 - t1)* 340 / 2) * 100))
    time.sleep(1)

    