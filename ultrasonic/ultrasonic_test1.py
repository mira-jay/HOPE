import lgpio as GPIO
import time

# set pins
TRIG = 23
ECHO = 24

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
	print("trig sent")
	
	
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
	#try:
	while True:
		dist = get_distance()
		print("Measured distance = {:.2f} cm".format(dist))
		time.sleep(1)
	# reset by pressing ctrl c
	#except KeyboardInterrupt:
		#("Measurement stopped by user")
		#GPIO.gpiochip_close(h)

