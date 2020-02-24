import serial

ser = serial.Serial("/dev/ttyS0", 9600 )  # Selects the TX Pin
servo =str(4)
while True:
    data = ("Fuck OFF ")
    ser.write(servo.encode())
    
ser.close()
