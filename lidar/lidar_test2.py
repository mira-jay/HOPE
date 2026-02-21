# remember, xarm_venv must be activated for code to work.
import os


from adafruit_rplidar import RPLidar

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


# set up the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, baudrate = 115200, timeout=3)

d_max: int = 500
i_min: int = 0
i_max: int = 50


def update_line(num, iterator, line):
    scan = next(iterator)

    offsets = np.array([(np.radians(meas[1]), meas[2]) for meas in scan])
    line.set_offsets(offsets)
    intents = np.array([meas[0] for meas in scan])
    line.set_array(intents)
    return line
     


try:
    plt.rcParams["toolbar"] = "None"
    fig = plt.figure()

    ax = plt.subplot(111, projection="polar")
    line = ax.scatter([0,0], [0,0], s=5, c=[i_min, i_max], cmap=plt.cm.Greys_r, lw=0)

    ax.set_rmax(d_max)

    ax.grid(True)

    iterator = lidar.iter_scans(max_buf_meas = 5000)
    ani = animation.FuncAnimation(fig, update_line, frames = 75, fargs = (iterator, line), interval = 50, blit= False, cache_frame_data = False)
    ani.save("lidar/lidar1.mp4", writer = "ffmpeg", fps = 15)



except KeyboardInterrupt:
    print("stopping.")
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()