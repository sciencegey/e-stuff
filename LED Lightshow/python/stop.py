#!/usr/bin/python

import sys, time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

r = 0
g = 0
b = 0

rLed = GPIO.PWM(2, 60)
gLed = GPIO.PWM(3, 60)
bLed = GPIO.PWM(4, 60)

rLed.start(r)
gLed.start(g)
bLed.start(b)

try:
	while True:
		time.sleep(1)

except KeyboardInterrupt:
	rLed.stop()
	bLed.stop()
	gLed.stop()
	GPIO.cleanup()