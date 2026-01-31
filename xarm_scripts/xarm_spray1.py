import xarm
import time

black = xarm.Controller("USB5306101095D182300023D4D4")

#set servos for black
black_servo1 = xarm.Servo(1, 340)
black_servo2 = xarm.Servo(2)
black_servo3 = xarm.Servo(3)
black_servo4 = xarm.Servo(4)
black_servo5 = xarm.Servo(5, 500)
black_servo6 = xarm.Servo(6, 100)

black.setPosition([black_servo1, black_servo2, black_servo3, black_servo4, black_servo5, black_servo6], wait = True)

black.setPosition(1, 450, wait = True)