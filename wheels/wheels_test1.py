import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

def control_wheels(command):
    ser.write(command.encode('ascii'))
    print(f'Sent command: {command}')
    time.sleep(1)
    if ser.in_waiting > 0:
        response = ser.readline().decode('utf-8').strip()
        print(f'Arduino response: {response}')

if __name__ == "__main__":
    control_wheels('1')
    time.sleep(10)
    control_wheels('0')