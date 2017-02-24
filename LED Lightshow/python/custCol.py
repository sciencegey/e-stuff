#!/usr/bin/python

import sys, time, struct, math
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

col = sys.argv[1]

def hex2rgb(hex):
	return struct.unpack('BBB', hex.decode('hex'))

rgb = list(hex2rgb(col))
r = math.floor(rgb[0]/2.55)
g = math.floor(rgb[1]/2.55)
b = math.floor(rgb[2]/2.55)

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