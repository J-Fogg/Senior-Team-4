import pyximport; pyximport.install()
import RPi.GPIO as GPIO
import time

servoPIN = 2
servoPIN2 = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN2, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(7.0) # Initialization
t = GPIO.PWM(servoPIN2, 50) # GPIO 17 for PWM with 50Hz
t.start(12.3) # Initialization
try:
   while True:
     g = float(input("Duty Cycle1 = "))
     p.ChangeDutyCycle(g)
     i = float(input("Duty Cycle2 = "))
     t.ChangeDutyCycle(i)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()
