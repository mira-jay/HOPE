import xarm

arm = xarm.Controller("USB")

#servo1 = xarm.Servo(1)
servo2 = xarm.Servo(2)
servo3 = xarm.Servo(3)
servo4 = xarm.Servo(4)
servo5 = xarm.Servo(5, 880)
servo6 = xarm.Servo(6)

for i in range(3):
	arm.setPosition([servo2, servo3, servo4, servo5, servo6])
	for j in range(3):
		arm.setPosition([servo2, servo3])
		arm.setPosition([[1,1000], [2,0]])
	arm.setPosition([[3,300], [4,300]])
