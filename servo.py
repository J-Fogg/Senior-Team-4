import RPi.GPIO as GPIO
import time

servoPIN = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization
while True:

	Duty_Cycle = input("Duty Cycle = 0.5")
	if  (Duty_Cycle == 2.5) :
		p.ChangeDutyCycle(3)
	if  (Duty_Cycle == 7.5) :
		p.ChangeDutyCycle(8)
	if  (Duty_Cycle == 12.5) :
		p.ChangeDutyCycle(12)
