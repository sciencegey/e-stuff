import RPi.GPIO as GPIO
from random import randint
from time import sleep
GPIO.setmode(GPIO.BCM)

#Button Led Pins
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

#Button Pins
GPIO.setup(14, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

#Life Pins
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

score = 0
lives = 3
level = 1
fail = True
hold = False

lifePins = [7, 8, 25]
buttonPins = [14, 15, 18, 23]
ledPins = [2, 3, 4, 17]

def setLives(lives):
    #print("setting lives: ")
    for i in range(0, len(lifePins)):
        GPIO.output(lifePins[i], 0)
    for i in range(0, lives):
        GPIO.output(lifePins[i], 1)

def resetLights():
    #print("resetting lights: ")
    for i in range(0, len(ledPins)):
        GPIO.output(ledPins[i], 0)

def allOn():
    for i in range(0, len(ledPins)):
        GPIO.output(ledPins[i], 1)

try:
    while True:
        print("Playing")
        score = 0
        level = 1
        lives = 3
        setLives(int(lives))
        resetLights()
        while lives > 0:
            #print("lives ", lives)
            setLives(int(lives))
            button = randint(0,3)
            #print("button ", button)
            GPIO.output(ledPins[int(button)], 1)
            #print("start")
            for i in range(0, 100):
                if GPIO.input(buttonPins[int(button)]) == 1:
                    print("Congrats!")
                    fail = False
                    break
                else:
                    #print("fail")
                    sleep(0.1 / (level/2))
            if fail == True:
                print("Try again!")
                lives -= 1
                score -= 1
                print("Lives remaining:", lives)
            else:
                score += 1
                level += 1
                print("Current score:", score)
                sleep(1)
            resetLights()
            sleep(1)
            fail = True
            print("Level: ", level)
        setLives(0)
        print("You finished with a score of ", int(score), "!")
        hold = True
        print("")
        print("Press Any Button to Start!")
        allOn()
        while hold == True:
            for i in range(0, 200):
                for i in range(0, len(buttonPins)):
                    if GPIO.input(buttonPins[i]) == 1:
                        hold = False
                        break
                sleep(0.01)
            resetLights()
            for i in range(0, 200):
                for i in range(0, len(buttonPins)):
                    if GPIO.input(buttonPins[i]) == 1:
                        hold = False
                        break
                sleep(0.01)
            allOn()
except:
    print("Goodbye!")
    GPIO.cleanup()