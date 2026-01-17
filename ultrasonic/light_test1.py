import lgpio as GPIO
import time

LED_PIN = 18

h = GPIO.gpiochip_open(0)

try:
    while True:
        GPIO.gpio_write(h, LED_PIN, 1)
        time.sleep(0.00001)
        GPIO.gpio_write(h, LED_PIN, 0)
except KeyboardInterrupt:
    GPIO.gpiochip_close(h)
