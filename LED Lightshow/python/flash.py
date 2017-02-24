#!/usr/bin/python

import sys, struct, math
import RPi.GPIO as GPIO
from random import randint
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

type = sys.argv[1]
time = int(sys.argv[2])

def hex2rgb(hex):
    return struct.unpack('BBB', hex.decode('hex'))

if type == "c":
	rgb = list(hex2rgb(sys.argv[3]))
	r = math.floor(rgb[0]/2.55)
	g = math.floor(rgb[1]/2.55)
	b = math.floor(rgb[2]/2.55)
elif type == "r":
	r = 0
	g = 0
	b = 0

rLed = GPIO.PWM(2, 60)
gLed = GPIO.PWM(3, 60)
bLed = GPIO.PWM(4, 60)

colBias = 0

rLed.start(r)
gLed.start(g)
bLed.start(b)

try:
	while True:
		if type == "c":
			rLed.ChangeDutyCycle(r)
			gLed.ChangeDutyCycle(g)
			bLed.ChangeDutyCycle(b)
			sleep(0.1*time)
			rLed.ChangeDutyCycle(0)
			gLed.ChangeDutyCycle(0)
			bLed.ChangeDutyCycle(0)
			sleep(0.1*time)
		elif type == "r":
			colBias = randint(1,3)
			if colBias == 1:
				rColRand = randint(70,99)
				bColRand = randint(1,30)
				gColRand = randint(1,30)
			elif colBias == 2:
				rColRand = randint(1,30)
				bColRand = randint(70,99)
				gColRand = randint(1,30)
			elif colBias == 3:
				rColRand = randint(1,30)
				bColRand = randint(1,30)
				gColRand = randint(70,99)
			else:
				rColRand = randint(1,99)
				bColRand = randint(1,99)
				gColRand = randint(1,99)
			r = randint(1,rColRand)
			g = randint(1,gColRand)
			b = randint(1,bColRand)
			rLed.ChangeDutyCycle(r)
			gLed.ChangeDutyCycle(g)
			bLed.ChangeDutyCycle(b)
			sleep(0.1*time)
			rLed.ChangeDutyCycle(0)
			gLed.ChangeDutyCycle(0)
			bLed.ChangeDutyCycle(0)
			sleep(0.1*time)

except KeyboardInterrupt:
	rLed.stop()
	bLed.stop()
	gLed.stop()
	GPIO.cleanup()