import time

from motor_setup import setup

interface, motors, head = setup()

while True:
	angle = float(input("Enter a angle to rotate (in radians): "))

	interface.startLogging('position_logs.log')
	interface.increaseMotorAngleReferences([head],[angle])

	while not interface.motorAngleReferencesReached([head]) :
		time.sleep(0.1)

	print "Destination reached!"

interface.stopLogging('position_logs.log')
interface.terminate()
