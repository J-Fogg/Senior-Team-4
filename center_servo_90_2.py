import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
kit.servo[7].actuation_range = 180
kit.servo[7].angle = 180