import robot 
from motor_setup import setup

interface, motors = setup()

r = robot.Robot(interface, motors)

r.follow()

interface.terminate()
