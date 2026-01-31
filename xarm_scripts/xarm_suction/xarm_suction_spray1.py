# This code programs the motion of the blue and black arms
# Pick up the patch, bring it around, spray it with adhesive
# This assumes the patch is the same size as the paper test
# Will need to be modified to accomodate true patch dimensions

import xarm
from suction import suction_test1
import time

# Initialization
blue = xarm.Controller("USBD30F103095D182300023D4D4")
black = xarm.Controller("USB5306101095D182300023D4D4")
suction_test1.init()

# Checks connection of arms
print("Battery voltage of blue: ", blue.getBatteryVoltage())
print("Battery voltage of black: ", black.getBatteryVoltage())

# Black default positions
black_servo1 = xarm.Servo(1, 380)
black_servo2 = xarm.Servo(2, 436)
black_servo3 = xarm.Servo(3, 500)
black_servo4 = xarm.Servo(4, 500)
black_servo5 = xarm.Servo(5, 500)
black_servo6 = xarm.Servo(6, 500)
black.setPosition([black_servo1, black_servo2, black_servo3, black_servo4, black_servo5, black_servo6], wait = True)

# Blue default positions
# Note that there is no servo1 - no claw
blue_servo2 = xarm.Servo(2)
blue_servo3 = xarm.Servo(3, 883)
blue_servo4 = xarm.Servo(4, 500)
blue_servo5 = xarm.Servo(5, 500)
blue_servo6 = xarm.Servo(6, 550)
# No need to modify servo2 - will stay constant
blue.setPosition([blue_servo3, blue_servo4, blue_servo5, blue_servo6], wait = True)

# Grab the patch
blue.setPosition(5, 500, wait=True)
blue.setPosition(6, 150, wait=True)
blue.setPosition(4, 830, wait = True)
blue.setPosition(3, 138, wait = 5.00)
suction_test1.control_motor("h")
suction_test1.control_motor("f")
time.sleep(5.00)

# Take it out
blue.setPosition(3, 870, wait = True)
blue.setPosition(4, 570, wait = True)
blue.setPosition(6, 500, wait = True)
time.sleep(1.00)
suction_test1.control_motor("s")




# Black position to spray
black.setPosition(6, 200, wait = True)
black.setPosition(3, 120, wait = True)
black.setPosition(2, 490, wait = True)
