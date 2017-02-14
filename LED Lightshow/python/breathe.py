#!/usr/bin/python

import sys, time, struct, math
from random import randint
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

col = sys.argv[1]
timeMult = int(sys.argv[2])

def hex2rgb(hex):
    return struct.unpack('BBB', hex.decode('hex'))

rLed = GPIO.PWM(2, 60)
gLed = GPIO.PWM(3, 60)
bLed = GPIO.PWM(4, 60)

run = False
up = False

rgb = list(hex2rgb(col))
rCol = math.floor(rgb[0]/2.55)
r = 0
gCol = math.floor(rgb[1]/2.55)
g = 0
bCol = math.floor(rgb[2]/2.55)
b = 0
bInt = (float(bCol) / 3) / timeMult
gInt = (float(gCol) / 3) / timeMult
rInt = (float(rCol) / 3) / timeMult

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
			r = 0
			g = 0
			b = 0
			run = True
			up = True

except KeyboardInterrupt:
	rLed.stop()
	bLed.stop()
	gLed.stop()
	GPIO.cleanup()