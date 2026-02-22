# this is the code for the video
from suction import motor_driver_test1
import time
import xarm

#initialization
motor_driver_test1.init()
black = xarm.Controller("USB5306101095D182300023D4D4")
blue = xarm.Controller("USBD30F103095D182300023D4D4")


#set servos for blue
blue_servo2 = xarm.Servo(2)
blue_servo3 = xarm.Servo(3)
blue_servo4 = xarm.Servo(4)
blue_servo5 = xarm.Servo(5)
blue_servo6 = xarm.Servo(6)

#set servos for black
black_servo1 = xarm.Servo(1)
black_servo2 = xarm.Servo(2)
black_servo3 = xarm.Servo(3)
black_servo4 = xarm.Servo(4)
black_servo5 = xarm.Servo(5)
black_servo6 = xarm.Servo(6)

# set default position for blue (do s5 before s6)
blue.setPosition(5, 1000, wait=True)
blue.setPosition(6, 136, wait=True)
blue.setPosition(4, 486, wait = True)
blue.setPosition(3, 103, wait = True)
blue.setPosition(2, 679, wait = True)

# set default for black
black.setPosition(5, 881, wait=True)
# s6 is not moving
black.setPosition(4, 488, wait = True)
black.setPosition(3, 859, wait = True)
black.setPosition(2, 462, wait = True)
black.setPosition(1, 315, wait = True)

# blue dispense sponge
blue.setPosition(5, 1000, wait=True)
blue.setPosition(4, 486, wait = True)
blue.setPosition(3, 103, wait = True)
motor_driver_test1.set_speed("h")
motor_driver_test1.M2("f")
time.sleep(5.00)
motor_driver_test1.M2("b")
time.sleep(5.00)
motor_driver_test1.M2("s")
time.sleep(5.00)

# blue grab patch
blue.setPosition(6, 865, 2000, wait=True)
blue.setPosition(5, 500, 2000, wait = True)
blue.setPosition(4, 900, 2000, wait = True)
blue.setPosition(3, 100, 2000, wait =True)
motor_driver_test1.M1("f")
time.sleep(20.00)

# blue spray position
#blue.setPosition(5, 600, wait=True)
blue.setPosition(4, 362, 2000, wait=True)
blue.setPosition(3, 751, 2000, wait=True)
blue.setPosition(6, 490, 2000, wait = True)
blue.setPosition(5, 870, 2000, wait = True)

# black spray
black.setPosition(4, 495, wait = True)
black.setPosition(3, 830, wait = True)
black.setPosition(2, 433, wait = True)
black.setPosition(1, 400, wait = True)
black.setPosition(1, 315, wait=True)
time.sleep(2.00)

# blue place patch
blue.setPosition(6, 136, 2000, wait=True)
blue.setPosition(5, 1000, 2000, wait=True)
blue.setPosition(4, 486, 2000, wait = True)
blue.setPosition(3, 103, 2000, wait = True)
time.sleep(3.00)
motor_driver_test1.M1("s")