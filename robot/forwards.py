import robot 
from motor_setup import setup

interface, motors, head = setup()

r = robot.Robot(interface, motors)

while True:
	amount = input('enter a distance ')
	r.rotate_head(amount)

interface.terminate()
