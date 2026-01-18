import xarm
import time

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
blue.setPosition(3, 138, wait = True)
time.sleep(5.00)

#take it out
blue.setPosition(3, 870, wait = True)
blue.setPosition(4, 570, wait = True)
blue.setPosition(6, 540, wait = True)
blue.setPosition(5, 1000, wait = True)
#with this code, an air pump can be added to provide suction.


