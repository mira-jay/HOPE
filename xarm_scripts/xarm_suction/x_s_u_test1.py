from suction import suction_test1
from ultrasonic import ultrasonic_test2
import time
import xarm

#initialization
suction_test1.init()
blue = xarm.Controller("USBD30F103095D182300023D4D4")

#set servos for blue
blue_servo2 = xarm.Servo(2)
blue_servo3 = xarm.Servo(3)
blue_servo4 = xarm.Servo(4)
print("servo4: ", blue.getPosition(blue_servo4))
blue_servo5 = xarm.Servo(5)
print("servo5: ", blue.getPosition(blue_servo5))
blue_servo6 = xarm.Servo(6)

#grab the patch
blue.setPosition(5, 500, wait=True)
blue.setPosition(6, 150, wait=True)
blue.setPosition(4, 830, wait = True)
blue.setPosition(3, 138, wait = 5.00)
suction_test1.control_motor("h")
suction_test1.control_motor("f")
time.sleep(5.00)

#take it out
blue.setPosition(3, 870, wait = True)
blue.setPosition(4, 570, wait = True)
blue.setPosition(6, 540, wait = True)
blue.setPosition(5, 1000, wait = True)
time.sleep(1.00)
suction_test1.control_motor("s")
distance = ultrasonic_test2.get_distance()
print(distance)
