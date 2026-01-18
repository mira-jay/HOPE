import xarm

arm = xarm.Controller("USB")

servo1 = xarm.Servo(1) #assumes default unit position 500
servo2 = xarm.Servo(2, 300) #unit position 300
servo3 = xarm.Servo(3, 90.0) #angle 90 degrees

#sets servo1 to unit position 300 and waits default 1 second before returning
arm.setPosition(1, 300, wait=True)

#sets servo2 to unit position 700 and moves the servo at a rate of 2 seconds
arm.setPosition(2, 700, 2000, True)

#sets servo1 to 45 degrees and waits default 1 second before returning
arm.setPosition(3, 45.0, wait=True)

#sets servo2 to position 300 as defined above but continues to the next method before
#completing movement
arm.setPosition(servo2)

#sets servos 1-3 as defined and continues without waiting
arm.setPosition([servo1, servo3])

#sets servo 1 to unit position 200 and servo2 to 90 degrees
arm.setPosition([[1, 200], [2, 90.0]], wait=True)

#servo object and servo ID/position pairs can be combined
arm.setPosition([servo1, [2, 500], [3, 0.0]], 2000)
