#!/usr/bin/python

import sys, time, struct, math
from random import randint
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

timeMult = int(sys.argv[1])

rLed = GPIO.PWM(2, 60)
gLed = GPIO.PWM(3, 60)
bLed = GPIO.PWM(4, 60)

run = False
up = False

rCol = randint(0,90)
r = 0
rInt = 0
gCol = randint(0,90)
g = 0
gInt = 0
bCol = randint(0,90)
b = 0
bInt = 0

colBias = 0

rLed.start(r)
gLed.start(g)
bLed.start(b)

try:
	while True:
		while run:
			if up:
				r += rInt
				g += gInt
				b += bInt
				if r >= rCol:
					r = rCol
				if g >= gCol:
					g = gCol
				if b >= bCol:
					b = bCol
				if r == rCol and g == gCol and b == bCol:
					up = False
					time.sleep(0.5*timeMult)
				else:
					r -= rInt
					g -= gInt
					b -= bInt
				if r <= 0:
					r = 0
				if g <= 0:
					g = 0
				if b <= 0:
					b = 0
				if r == 0 and g == 0 and b == 0:
					run = False
			rLed.ChangeDutyCycle(r)
			gLed.ChangeDutyCycle(g)
			bLed.ChangeDutyCycle(b)
			time.sleep(0.05)
		time.sleep(1)
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
		rCol = randint(1,rColRand)
		r = 0
		rInt = (float(rCol) / 3) / timeMult
		gCol = randint(1,gColRand)
		g = 0
		gInt = (float(gCol) / 3) / timeMult
		bCol = randint(1,bColRand)
		b = 0
		bInt = (float(bCol) / 3) / timeMult
		run = True
		up = True

except KeyboardInterrupt:
	rLed.stop()
	bLed.stop()
	gLed.stop()
	GPIO.cleanup()