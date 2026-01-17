import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2) #wait for arduino to reset

def send_command(cmd):
	arduino.write(cmd.encode())
	print("Sent: ", cmd)
	response = arduino.readline().decode().strip()
	print("Arduino: ", response)


while True:
	command = input("> ").strip().lower()
	if command == 'q':
		print("Exiting...")
		break
	if command:
		send_command(command)

