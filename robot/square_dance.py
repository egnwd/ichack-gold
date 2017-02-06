#!/usr/bin/env python

import time
import sys
import robot
from motor_setup import setup

interface, motors = setup()

m = robot.Robot(interface, motors)

while True:
	raw_input('hit a key...')
	for i in range(0,4):
		m.forward(20)
		m.rotate(90)

interface.terminate()

