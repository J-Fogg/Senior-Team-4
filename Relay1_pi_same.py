import RPi.GPIO as GPIO

relayPIN = 5
GPIO.setmode(GPIO.BOARD) # To use BCM Mode use GPIO.BCM
GPIO.setup(relayPIN, GPIO.OUT) 
try:
   while True:
     g = int(input("Relay = "))
     GPIO.output(relayPIN, g)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()
