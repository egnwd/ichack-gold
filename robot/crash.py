import robot 
import time
from motor_setup import setup

interface, motors = setup()

m = movement.Movement(interface, motors)
r = robot.Robot(interface, motors)

r.drive()
while True:
	bl = r.bumpLeft()
	br = r.bumpRight()
	
	if bl and br:
		r.recover(Robot.Forward)
	elif bl:
		r.recover(Robot.Left)
	elif br:
		r.recover(Robot.Right)

	time.sleep(0.1)

interface.terminate()
