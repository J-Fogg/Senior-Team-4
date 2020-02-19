import time
from adafruit_servokit import ServoKit
import adafruit_pca9685
import board
import busio
import numpy as np
import imutils
kit = ServoKit(channels=16)
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)
hat.frequency = 60
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
Step = .1
Pos = 90
Start= 0
while(1):
    if Pos >= 170:
        Step *= -1
        
    elif Pos <= 10:
        Step *= -1
    Pos += Step
    #time.sleep(.1)
    kit.servo[3].angle = Pos
        
    


