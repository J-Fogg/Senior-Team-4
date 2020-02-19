import serial

ser = serial.Serial ("/dev/ttyS0", 9600 )  # Selects the TX Pin 
while True:
	data = ("Hello World ")
	ser.write(data.encode())


