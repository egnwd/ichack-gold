import brickpi

def setup():
	interface=brickpi.Interface()
	interface.initialize()
	
	#interface.startLogging('position_logs.log')
	
	motors = [0,1]
	
	interface.motorEnable(motors[0])
	interface.motorEnable(motors[1])
	
	velocityLimit = 12.0
	accelerationLimit = 6.0
	
	motor0Params = interface.MotorAngleControllerParameters()
	
	motor0Params.maxRotationAcceleration = accelerationLimit
	motor0Params.maxRotationSpeed = velocityLimit
	motor0Params.feedForwardGain = 255/20.0
	motor0Params.minPWM = 18.0
	motor0Params.pidParameters.minOutput = -255
	motor0Params.pidParameters.maxOutput = 255
	motor0Params.pidParameters.k_p = 510.0
	motor0Params.pidParameters.k_i = 361.0
	motor0Params.pidParameters.k_d = 18.0
	
	motor1Params = interface.MotorAngleControllerParameters()
	
	motor1Params.maxRotationAcceleration = accelerationLimit
	motor1Params.maxRotationSpeed = velocityLimit
	motor1Params.feedForwardGain = 255/20.0
	motor1Params.minPWM = 18.0
	motor1Params.pidParameters.minOutput = -255
	motor1Params.pidParameters.maxOutput = 255
	motor1Params.pidParameters.k_p = 510.0
	motor1Params.pidParameters.k_i = 326.0
	motor1Params.pidParameters.k_d = 20.0
	
	interface.setMotorAngleControllerParameters(motors[0],motor0Params)
	interface.setMotorAngleControllerParameters(motors[1],motor1Params)

	return interface, motors
