from picamera2 import Picamera2
import datetime
import rpicam

picam2 = Picamera2()


def record():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
    picam2.start_recording(f"video_{timestamp}.mp4")

def stop_record():
    picam2.stop_recording()