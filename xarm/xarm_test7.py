import xarm

blue = xarm.Controller("USBD30F103095D182300023D4D4")

#set servos for blue
blue_servo2 = xarm.Servo(2)
blue_servo3 = xarm.Servo(3, 100)
blue_servo4 = xarm.Servo(4, 483)
print("servo4: ", blue.getPosition(blue_servo4))
blue_servo5 = xarm.Servo(5)
print("servo5: ", blue.getPosition(blue_servo5))
blue_servo6 = xarm.Servo(6, 883)


#blue.setPosition([blue_servo2, blue_servo3, blue_servo4, blue_servo5, blue_servo6], wait=True)
blue.setPosition(5, 500, wait=True)
print("servo5: ", blue.getPosition(blue_servo5))
blue.setPosition(4, 500, wait=True)
print("servo4: ", blue.getPosition(blue_servo4))
#blue.setPosition(5, 500, wait = True)
#blue.setPosition(6, 103, wait = True)
#blue.setPosition(4, 876, wait=True)
