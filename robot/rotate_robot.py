import time

from motor_setup import setup

interface, motors = setup()

def	rotateLeft():
	angle = 4.8
	interface.increaseMotorAngleReferences(motors,[angle,-angle])

def	rotateRight():
	angle = 4.8
	interface.increaseMotorAngleReferences(motors,[-angle,angle])


while True:
	raw_input('hit a key...')
	for i in range(0,4):
		rotateLeft()
		time.sleep(1.6)

	# rotateRight()
	# time.sleep(1.6)

interface.terminate()

