import RPi.GPIO as GPIO
import time
import keyboard

#Pins are defined

RoAPin = 38    # pin11
RoBPin = 37    # pin12
RoSPin = 40    # pin13

#Global counter that stores the rotary event. +1 for every clockwise step and -1 for every anticlockwise step.

globalCounter = 0

flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(RoAPin, GPIO.IN)    # input mode
	GPIO.setup(RoBPin, GPIO.IN)
	GPIO.setup(RoSPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	rotaryClear()

def rotaryDeal():
	global flag
	global Last_RoB_Status
	global Current_RoB_Status
	global globalCounter
	Last_RoB_Status = GPIO.input(RoBPin)
	while(not GPIO.input(RoAPin)):
		Current_RoB_Status = GPIO.input(RoBPin)
		flag = 1
	if flag == 1:
		flag = 0
		if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
			globalCounter = globalCounter + 1
			keyboard.press_and_release('down') #Change this to define, action to any clockwise rotary step event, here I've used as down arrow key.
		if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
			globalCounter = globalCounter - 1
			keyboard.press_and_release('up') #Change this to define, action to any clockwise rotary step event, here I've used as up arrow key.

def clear(ev=None):
        globalCounter = 0 #this resets the global counter
	keyboard.press_and_release('enter')  #Change this to define the action to be done if the switch is pressed,here it is set to 
                                             #act as 'enter' key of the keyboard

def rotaryClear():
        GPIO.add_event_detect(RoSPin, GPIO.FALLING, callback=clear) # wait for falling


def loop():
	global globalCounter
	while True:
		rotaryDeal()
#		print 'globalCounter = %d' % globalCounter

def destroy():
	GPIO.cleanup()             # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()
