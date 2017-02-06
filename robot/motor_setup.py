import brickpi

def setup():
	interface=brickpi.Interface()
	interface.initialize()

	#interface.startLogging('position_logs.log')
	
	motors = [0,1,2]
	
	interface.motorEnable(motors[0])
	interface.motorEnable(motors[1])
	interface.motorEnable(motors[2])
	
	velocityLimit = 12.0
	accelerationLimit = 6.0

	motor0Params = interface.MotorAngleControllerParameters()

	motor0Params.maxRotationAcceleration = accelerationLimit
	motor0Params.maxRotationSpeed = velocityLimit
	motor0Params.feedForwardGain = 265/20.0
	motor0Params.minPWM = 18.0
	motor0Params.pidParameters.minOutput = -255
	motor0Params.pidParameters.maxOutput = 255
	motor0Params.pidParameters.k_p = 450.0
	motor0Params.pidParameters.k_i = 348.8
	motor0Params.pidParameters.k_d = 14.5

	motor1Params = interface.MotorAngleControllerParameters()

	motor1Params.maxRotationAcceleration = accelerationLimit
	motor1Params.maxRotationSpeed = velocityLimit
	motor1Params.feedForwardGain = 255/20.0
	motor1Params.minPWM = 18.0
	motor1Params.pidParameters.minOutput = -255
	motor1Params.pidParameters.maxOutput = 255
	motor1Params.pidParameters.k_p = 450.0
 	motor1Params.pidParameters.k_i = 352.9
	motor1Params.pidParameters.k_d = 14.5
	
	motor2Params = interface.MotorAngleControllerParameters()
	
	motor2Params.maxRotationAcceleration = accelerationLimit
	motor2Params.maxRotationSpeed = velocityLimit
	motor2Params.feedForwardGain = 255/20.0
	motor2Params.minPWM = 18.0
	motor2Params.pidParameters.minOutput = -255
	motor2Params.pidParameters.maxOutput = 255
	motor2Params.pidParameters.k_p = 180.0
 	motor2Params.pidParameters.k_i = 100.0
	motor2Params.pidParameters.k_d = 7.65
	
	interface.setMotorAngleControllerParameters(motors[0],motor0Params)
	interface.setMotorAngleControllerParameters(motors[1],motor1Params)
	interface.setMotorAngleControllerParameters(motors[2],motor1Params)

	return interface, motors[:2], motors[2]

def generate_vals(k_u, period):
	k_p = 0.6 * k_u
	k_i = 2 * k_p / period
	k_d = k_p * period / 8
	return k_p, k_i, k_d
