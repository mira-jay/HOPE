import xarm

# arm is the first xArm detected which is connected to USB
arm = xarm.Controller('USB')
print("Battery voltage in volts:", arm.getBatteryVoltage())

