import time
import robot
from motor_setup import setup

interface, motors, head = setup()

r = robot.Robot(interface, motors)

while True:
	amount = input('enter a rotation ')
	r.forward(20)
	r.rotate(amount*2)
	r.forward(20)
	r.rotate(amount*2)

interface.terminate()
