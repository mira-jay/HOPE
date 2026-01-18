import xarm

arm = xarm.Controller("USB")

servo1 = xarm.Servo(1, 500)
servo2 = xarm.Servo(2, 0)
servo3 = xarm.Servo(3)
servo4 = xarm.Servo(4)
servo5 = xarm.Servo(5, 880)
servo6 = xarm.Servo(6)

arm.setPosition([servo1, servo2, servo3, servo4, servo5, servo6])

