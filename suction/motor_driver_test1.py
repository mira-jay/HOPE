# This test can control multiple motors from the 4WD Pi motor HAT

import lgpio as GPIO
from time import sleep

#define the pin for drv8833#1
NSLEEP1 = 12  #Enabling signal pin for drv8833
AN11 = 17
AN12 = 27
BN11 = 22
BN12 = 23
#define the pin for drv8833#2
NSLEEP2 = 13
AN21 = 24
AN22 = 25
BN21 = 26
BN22 = 16

h = None
temp1=1
p1 = None
p2 = None

def init():

    global h, p1, p2, temp1
    h = GPIO.gpiochip_open(0)

    #Define pin as output signal
    GPIO.gpio_claim_output(h, NSLEEP1)
    GPIO.gpio_claim_output(h, NSLEEP2)
    GPIO.gpio_claim_output(h, AN11)
    GPIO.gpio_claim_output(h, AN12)
    GPIO.gpio_claim_output(h, BN11)
    GPIO.gpio_claim_output(h, BN12)
    GPIO.gpio_claim_output(h, AN21)
    GPIO.gpio_claim_output(h, AN22)
    GPIO.gpio_claim_output(h, BN21)
    GPIO.gpio_claim_output(h, BN22)

    #Initialize the motor drive signal so that the motor is in a stopped state
    GPIO.gpio_write(h, AN11, 0)
    GPIO.gpio_write(h, AN12, 0)
    GPIO.gpio_write(h, BN11, 0)
    GPIO.gpio_write(h, BN12, 0)
    GPIO.gpio_write(h, AN21, 0)
    GPIO.gpio_write(h, AN22, 0)
    GPIO.gpio_write(h, BN21, 0)
    GPIO.gpio_write(h, BN22, 0)

    p1=GPIO.tx_pwm(h, NSLEEP1, 1000, 20)#Define p1 as a pulse signal of 1000 Hz and duty cycle of 30%
    p2=GPIO.tx_pwm(h, NSLEEP2, 1000, 20)#Define p2 as a pulse signal of 1000 Hz and duty cycle of 30%


def M1(x):
    global p1, p2, temp1

    if h is None:
        raise RuntimeError("Motor system not initialized. Call init() first.")

    if x=='f':
        print("forward")
        GPIO.gpio_write(h, AN11, 1)
        GPIO.gpio_write(h, AN12, 0)
        temp1=1
        x='z'
    elif x=='b':
        print("backward")
        GPIO.gpio_write(h, AN11, 0)
        GPIO.gpio_write(h, AN12, 1)
        temp1=0
        x='z'
    elif x=='s':
        print("stop")
        GPIO.gpio_write(h, AN11, 0)
        GPIO.gpio_write(h, AN12, 0)
        x='z'
        

def M2(x):
    global p1, p2, temp1

    if h is None:
        raise RuntimeError("Motor system not initialized. Call init() first.")

    if x=='f':
        print("forward")
        GPIO.gpio_write(h, BN11, 1)
        GPIO.gpio_write(h, BN12, 0)
        temp1=1
        x='z'
    elif x=='b':
        print("backward")
        GPIO.gpio_write(h, BN11, 0)
        GPIO.gpio_write(h, BN12, 1)
        temp1=0
        x='z'
    elif x=='s':
        print("stop")
        GPIO.gpio_write(h, BN11, 0)
        GPIO.gpio_write(h, BN12, 0)
        x='z'

def M3(x):
    global p1, p2, temp1

    if h is None:
        raise RuntimeError("Motor system not initialized. Call init() first.")

    if x=='f':
        print("forward")
        GPIO.gpio_write(h, AN21, 1)
        GPIO.gpio_write(h, AN22, 0)
        temp1=1
        x='z'
    elif x=='b':
        print("backward")
        GPIO.gpio_write(h, AN21, 0)
        GPIO.gpio_write(h, AN22, 1)
        temp1=0
        x='z'
    elif x=='s':
        print("stop")
        GPIO.gpio_write(h, AN21, 0)
        GPIO.gpio_write(h, AN22, 0)
        x='z'

def M4(x):
    global p1, p2, temp1

    if h is None:
        raise RuntimeError("Motor system not initialized. Call init() first.")

    if x=='f':
        print("forward")
        GPIO.gpio_write(h, BN21, 1)
        GPIO.gpio_write(h, BN22, 0)
        temp1=1
        x='z'
    elif x=='b':
        print("backward")
        GPIO.gpio_write(h, BN21, 0)
        GPIO.gpio_write(h, BN22, 1)
        temp1=0
        x='z'
    elif x=='s':
        print("stop")
        GPIO.gpio_write(h, BN21, 0)
        GPIO.gpio_write(h, BN22, 0)
        x='z'



def set_speed(x):

    global p1, p2, temp1

    if h is None:
        raise RuntimeError("Motor system not initialized. Call init() first.")

   
    if x=='l':
        print("low")
        p1=GPIO.tx_pwm(h, NSLEEP1, 1000, 30) #Set the P1 pulse signal duty cycle to 30%
        p2=GPIO.tx_pwm(h, NSLEEP2, 1000, 30) #Set the P2 pulse signal duty cycle to 30%
        x='z'
    elif x=='m':
        print("medium")
        p1=GPIO.tx_pwm(h, NSLEEP1, 1000, 60) #Set the P1 pulse signal duty cycle to 60%
        p2=GPIO.tx_pwm(h, NSLEEP2, 1000, 60) #Set the P2 pulse signal duty cycle to 60%
        x='z'
    elif x=='h':
        print("high")
        p1=GPIO.tx_pwm(h, NSLEEP1, 1000, 90) #Set the P1 pulse signal duty cycle to 90%
        p2=GPIO.tx_pwm(h, NSLEEP2, 1000, 90) #Set the P2 pulse signal duty cycle to 90%
        x='z'


'''


init()
set_speed("h")
M1("r")
M1("f")
sleep(5.00)
#M2("b")
sleep(5.00)
M1("s")

'''