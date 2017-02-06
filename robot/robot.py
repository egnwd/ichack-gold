import time
import math
import brickpi

class Robot:

	#degree = 6.0 / 89.0 
	degree = 7.05 / 92.0
	degree_head = 5.0 / 300.0 
	#cm = 20.0 / 41.9
	cm = 30.0 / 62.5
	speed = 5.0
	garbage = 255

	def __init__(self, interface, motors, sonar=3, head=2, bumper0=0, bumper1=1):
		self._interface = interface
		self._motors = motors
		self._interface.sensorEnable(sonar, brickpi.SensorType.SENSOR_ULTRASONIC);
		self._sonar = sonar
		self._head = [head]
		#self._prev_sonar = Robot.garbage
		self._sonar_ma = []
		self._interface.sensorEnable(bumper0, brickpi.SensorType.SENSOR_TOUCH);
		self._interface.sensorEnable(bumper1, brickpi.SensorType.SENSOR_TOUCH);
		self._bumper = [bumper0, bumper1]

	def	rotate(self, angle):
		angle *= Robot.degree
		self._interface.increaseMotorAngleReferences(self._motors,[-angle,angle])
		self.wait(self._motors)

	def rotate_head(self, angle):
		angle *= Robot.degree_head
		self._interface.increaseMotorAngleReferences(self._head, [angle])
		self.wait(self._head)
	
	def forward(self, n):
		distance = n * Robot.cm
		self._interface.increaseMotorAngleReferences(
				self._motors, [distance, distance]
		)
		self.wait(self._motors)

	def drive(self, reverse=False):
		v = Robot.speed * (-1 if reverse else 1)
		self._interface.setMotorRotationSpeedReferences(self._motors, [v,v])

	def drive_until_crash(self, reverse=False):
		v = Robot.speed * (-1 if reverse else 1)
		angles_prev = self._interface.getMotorAngleReferences(self._motors)
		self._interface.setMotorRotationSpeedReferences(self._motors, [v,v])
		while True:
			pressed0 = self._interface.getSensorValue(self._bumper[0])
			pressed1 = self._interface.getSensorValue(self._bumper[1])
			if pressed0[0] or pressed1[0]:
				# stop
				self._interface.setMotorPwm(self._motors[0],0)
				self._interface.setMotorPwm(self._motors[1],0)
				# self._interface.setMotorPwm(self._motors, [0.0,0.0])
				break
		self.forward(-15)
		angles_new = self._interface.getMotorAngleReferences(self._motors)
		return self.displacement(angles_prev, angles_new)

	def displacement(self, angles_prev, angles_new):
		motor0_diff = (angles_new[0] - angles_prev[0]) / Robot.cm
		motor1_diff = (angles_new[1] - angles_prev[1]) / Robot.cm
		return (motor0_diff + motor1_diff) / 2.0


	def sonar_distance(self):
		reading = Robot.garbage
		readings = []
		for _ in range(10):
			reading, _ = self._interface.getSensorValue(self._sonar)
			readings.append(reading)

		return readings[len(readings)/2]

		#if reading != Robot.garbage:
			#self._prev_sonar = reading
		#return self._prev_sonar

	def follow(self, desired=30):
		kp = 0.4

		while True:
			actual, _ = self._interface.getSensorValue(self._sonar)
			diff = 0.5 * kp * (actual - desired)
			v_r = self.speed + diff
			v_l = self.speed - diff
			self._interface.setMotorRotationSpeedReferences(self._motors, [v_l, v_r])
			time.sleep(0.01)

	def halt(self):
		self._interface.setMotorRotationSpeedReferences(self._motors, [0,0])
	
	def wait(self, motors):
		while not self._interface.motorAngleReferencesReached(motors):
			time.sleep(0.1)

