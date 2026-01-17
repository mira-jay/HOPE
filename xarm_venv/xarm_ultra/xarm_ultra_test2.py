import lgpio as GPIO
import time
import xarm

# set arm output location
arm = xarm.Controller("USB")

# set pins
TRIG = 23
ECHO = 24

# set arm starting location
servo1 = xarm.Servo(1, 90.0)
servo2 = xarm.Servo(2, 0.0)
servo3 = xarm.Servo(3, 90.0) # 0.0 degrees
servo4 = xarm.Servo(4, 0.0)
servo5 = xarm.Servo(5, 90.0) # formerly 880
servo6 = xarm.Servo(6, 90.0)
arm.setPosition([servo1, servo2, servo3, servo4, servo5, servo6], wait = True)


# open the gpio chip and set the gpio direction
h = GPIO.gpiochip_open(0)
GPIO.gpio_claim_output(h, TRIG)
GPIO.gpio_claim_input(h, ECHO)

def get_distance():
	# set trig low
	GPIO.gpio_write(h, TRIG, 0)
	time.sleep(2)
	
	
	# send 10us pulse to trig
	GPIO.gpio_write(h, TRIG, 1)
	time.sleep(0.00001)
	GPIO.gpio_write(h, TRIG, 0)
	
	
	# start recording the time when the wave is sent
	while GPIO.gpio_read(h, ECHO) == 0:
		pulse_start = time.time()
		
		
	# record time of arrival
	while GPIO.gpio_read(h, ECHO) == 1:
		pulse_end = time.time()
	

	# calculate the difference in times
	pulse_duration = pulse_end - pulse_start
	
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2 to avoid counting both distances there and back
	distance = pulse_duration * 17150
	distance = round(distance, 2)
	
	return distance

if __name__ == '__main__':
	try:
		time.sleep(5)
		dist = get_distance()
		print("Measured distance = {:.2f} cm".format(dist))
		while dist > 8.0:
			print("Distance is bigger than 8.0 cm")
			# find current angle
			current_pos3 = arm.getPosition(servo3, True)
			print("current pos of servo3: ", current_pos3)
			current_pos4 = arm.getPosition(servo4, True)
			print("current pos of servo4: ", current_pos4)
			# set position to current angle +/- 1 degree
			arm.setPosition([[3, current_pos3 - 10.0], [4, current_pos4 - 10.0]], wait = True)
			
			#arm.setPosition(1, current_pos3 + 10.0)
			#arm.setPosition(3, current_pos3 - 20.0)
			#arm.setPosition(4, current_pos4 - 10.0)
			dist = get_distance()
			print("Measured distance = {:.2f} cm".format(dist))
		print("reached!")
				
	# reset by pressing ctrl c
	except KeyboardInterrupt:
		print("action stopped by user")
		GPIO.gpiochip_close(h)
