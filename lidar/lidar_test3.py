from adafruit_rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'

lidar = RPLidar(None, PORT_NAME, baudrate=115200)

print(lidar.info)
print(lidar.health)

lidar.disconnect()