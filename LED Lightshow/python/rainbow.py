#!/usr/bin/python

import sys,  struct, math
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

r = 0
g = 99
b = 199

rUp = True
gUp = True
bUp = True

rLed = GPIO.PWM(2, 60)
gLed = GPIO.PWM(3, 60)
bLed = GPIO.PWM(4, 60)

rLed.start(r/2)
gLed.start(g/2)
bLed.start(b/2)

try:
	while True:
		if r >= 199:
			rUp = False
		elif r <= 0:
			rUp = True
		if g >= 199:
			gUp = False
		elif g <= 0:
			gUp = True
		if b >= 199:
			bUp = False
		elif b <= 0:
			bUp = True

		if rUp:
			r += 1
		else:
			r -= 1
		if gUp:
			g += 1
		else:
			g -= 1
		if bUp:
			b += 1
		else:
			b -= 1
		rLed.ChangeDutyCycle(r/2)
		gLed.ChangeDutyCycle(g/2)
		bLed.ChangeDutyCycle(b/2)
		sleep(0.05)

except KeyboardInterrupt:
	rLed.stop()
	bLed.stop()
	gLed.stop()
	GPIO.cleanup()