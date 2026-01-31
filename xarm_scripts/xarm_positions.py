import xarm

arm = xarm.Controller("USB")

servo1 = xarm.Servo(1)
servo2 = xarm.Servo(2)
servo3 = xarm.Servo(3)
servo4 = xarm.Servo(4)
servo5 = xarm.Servo(5)
servo6 = xarm.Servo(6)

print("servo1 angle: ", arm.getPosition(servo1))
print("servo2 angle: ", arm.getPosition(servo2))
print("servo3 angle: ", arm.getPosition(servo3))
print("servo4 angle: ", arm.getPosition(servo4))
print("servo5 angle: ", arm.getPosition(servo5))
print("servo6 angle: ", arm.getPosition(servo6))
