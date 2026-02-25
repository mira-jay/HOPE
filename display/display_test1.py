import subprocess
import time
import os

def show_image(image_path):
    print(f"displaying image: {image_path}")
    command = ["sudo", "fbi", "-a", "-T", "1", "--noverbose", image_path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process

def stop_image(process):
    if process:
        process.terminate()
        os.system("sudo pkill fbi")

if __name__ == "__main__":
    image = "/home/hope/hopedevice/SOAR_face.jpeg"
    
    process = show_image(image)
    time.sleep(10)
    stop_image(process)



