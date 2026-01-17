
import xarm

arm = xarm.Controller("USB")

servo1 = xarm.Servo(1)
servo2 = xarm.Servo(2)
servo3 = xarm.Servo(3)
servo4 = xarm.Servo(4)
servo5 = xarm.Servo(5)
servo6 = xarm.Servo(6)

position = arm.getPosition(1)
print("Servo1 pos: ", position)

position = arm.getPosition(2)
print("Servo2 pos: ", position)

position = arm.getPosition(3)
print("Servo3 pos: ", position)

position = arm.getPosition(4)
print("Servo4 pos: ", position)

position = arm.getPosition(5)
print("Servo5 pos: ", position)

position = arm.getPosition(6)
print("Servo6 pos: ", position)

