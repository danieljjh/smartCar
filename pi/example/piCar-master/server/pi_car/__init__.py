# -*- coding: UTF-8 -*-

'''
#=============================================================================
#     FileName: __init__.py
#         Desc: 
#       Author: wangheng
#        Email: wujiwh@gmail.com
#     HomePage: http://wangheng.org
#      Version: 0.0.1
#   LastChange: 2015-01-14 13:49:06
#      History:
#=============================================================================
'''
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
abort, render_template, flash
from contextlib import closing
import RPi.GPIO as GPIO
import time
import string
import serial

app = Flask(__name__)
app.config.from_object('pi_car.config.Development')

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('init.sql',mode='r') as f:
      ad.cursor().executescript(f.read())
    db.commit()


def init_car():
  #小车电机引脚定义
    IN1 = 20
    IN2 = 21
    IN3 = 19
    IN4 = 26
    ENA = 16
    ENB = 13

    #RGB三色灯引脚定义
    LED_R = 22
    LED_G = 27
    LED_B = 24 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)

    #设置pwm引脚和频率为2000hz
    pwm_ENA = GPIO.PWM(ENA, 2000)
    pwm_ENB = GPIO.PWM(ENB, 2000)
    pwm_ENA.start(0)
    pwm_ENB.start(0)
#@app.before_request
#def before_request():
#  g.db = connect_db()
#@app.teardown_request
#  def teardown_request(exception):
#  db = getattr(g, 'db', None)
#  if db is not None:
#    db.close()
#    g.db.close()

import  pi_car.views

if __name__=='__main__':
  app.run()
