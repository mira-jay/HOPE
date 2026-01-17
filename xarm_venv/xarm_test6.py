import xarm

blue = xarm.Controller("USBD30F103095D182300023D4D4")
black = xarm.Controller("USB5306101095D182300023D4D4")

print("Battery voltage of blue: ", blue.getBatteryVoltage())
print("Battery voltage of black: ", black.getBatteryVoltage())

#set servos for blue
blue_servo2 = xarm.Servo(2)
blue_servo3 = xarm.Servo(3, 100)
blue_servo4 = xarm.Servo(4)
blue_servo5 = xarm.Servo(5, 880)
blue_servo6 = xarm.Servo(6)

#set servos for black
black_servo1 = xarm.Servo(1, 300)
black_servo2 = xarm.Servo(2)
black_servo3 = xarm.Servo(3)
black_servo4 = xarm.Servo(4)
black_servo5 = xarm.Servo(5, 880)
black_servo6 = xarm.Servo(6)


black.setPosition(black_servo1)
blue.setPosition(blue_servo3)
