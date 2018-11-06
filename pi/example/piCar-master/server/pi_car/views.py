# -*- coding: UTF-8 -*-

'''
#=============================================================================
#     FileName: views.py
#         Desc: 
#       Author: wangheng
#        Email: wujiwh@gmail.com
#     HomePage: http://wangheng.org
#      Version: 0.0.1
#   LastChange: 2015-01-14 13:46:29
#      History:
#=============================================================================
'''
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from pi_car import app
import re
import RPi.GPIO as GPIO

CarSpeedControl = 50
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

@app.route('/')
def show_index():
	return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])                                   
def login():                                                                    
	if request.method=="GET":                                                   
		return "get"+request.form["user"]
	elif request.method=="POST":                                                
		return "post"

@app.route('/ctl',methods=['GET','POST'])
def ctrl_id():
    global pwm_ENA
    global pwm_ENB
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

    if request.method == 'POST':
		id=request.form['id']
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(11,GPIO.OUT)
		GPIO.setup(12,GPIO.OUT)
		GPIO.setup(15,GPIO.OUT)
		GPIO.setup(16,GPIO.OUT)

		if id == 't_left':
			t_left()
			return "left"
		elif id == 't_right':
			t_right()
			return "right"
		elif id == 't_up':
			t_up()
			return "up"
		elif id == 't_down':
			t_down()
			return "down"
		elif id == 't_stop':
			t_stop()
			return "stop"

    return redirect(url_for('show_index'))

def t_stop():
   GPIO.output(IN1, GPIO.LOW)
   GPIO.output(IN2, GPIO.LOW)
   GPIO.output(IN3, GPIO.LOW)
   GPIO.output(IN4, GPIO.LOW)

def t_up():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

def t_down():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

def t_left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

def t_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwm_ENA.ChangeDutyCycle(CarSpeedControl)
    pwm_ENB.ChangeDutyCycle(CarSpeedControl)

