import serial

ser = serial.Serial('/dev/ttyS0', 9600 , timeout=2) #, write_timeout=2) #blocking time out 2s
try:
  ser.close()
except serial.SerialException as err:
  print (err)
  print ("closing port")
  try:
    ser.close()
  except serial.SerialException as er2:
   print ("failed twice " + er2)
print ("Opening serial port")