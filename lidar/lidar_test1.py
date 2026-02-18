#code modeled after Dave Astels' RPILidar tutorial on Adafruit.

import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar


# set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
lcd = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
lcd.fill((0,0,0))
pygame.display.update()

# set up the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)

# scale data to fit on screen
max_distance = 0

# buffer to keep distance data each item stores measurement
# at each degree. Maintains most recent measurements.
scan_data = [0]*360

# using the iter_scans function, measurements can be accumulated
# and provide the angle and distance.

# once there's a scan, can step through each data point.
# the floor of the angle is taken and used as an index for
# the measurement. 

# process_data() can accomplish any number of functions,
# so long as it's as fast as possible.
# in this case it will display distance data.
def process_data(data):
    global max_distance
    lcd.fill((0,0,0))
    for angle in range(360):
        distance = data[angle]
        if distance > 0: 
             # ignore initially ungathered data
             max_distance = max([min([5000, distance]), max_distance])
             radians = angle * pi / 180.0
             x = distance * cos(radians)
             y = distance * sin(radians)
             point = (160 + int(x / max_distance * 119), 120 + int(y / max_distance * 119))
             lcd.set_at(point, pygame.Color(255, 255, 255))
    pygame.display.update()



try:
    print(lidar.info)
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process_data(scan_data)
except KeyboardInterrupt:
    print("stopping.")
lidar.stop()
lidar.disconnect()