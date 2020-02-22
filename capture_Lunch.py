import cv2
import numpy as np
import imutils
from simple_pid import PID
import time
import adafruit_pca9685
import board
import busio
import RPi.GPIO as GPIO
from imutils.video import VideoStream
i2c = busio.I2C(board.SCL, board.SDA)
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
hat = adafruit_pca9685.PCA9685(i2c)
hat.frequency = 60
relayPIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPIN, GPIO.OUT)


cap = VideoStream(src=-1).start()

Servo_Current = 90
AOE = 20
Max_Step_Size = 10
Servo_Channel = 2
Sweep_Step_Size = Max_Step_Size
kit.servo[Servo_Channel].angle = 90

while(1):

    # Take each frame
    frame = cap.read()
    dimensions = frame.shape    
    #Half = (dimensions[1]/2)
    #Deg = (90/Half)
    #Fin = Half * Deg
    #pid = PID(.2, 0.6, 4, setpoint=0)
    #pid.output_limits = (-90,90)
    

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


 
    lower_value1 = np.array([157,184,180])
    upper_value1 = np.array([192,225,218])

    lower_value3 = np.array([157,184,180])
    upper_value3 = np.array([192,225,218])


    mask_color1 = cv2.inRange(hsv, lower_value1, upper_value1)
    mask_color3 = cv2.inRange(hsv, lower_value3, upper_value3)
    mask = mask_color1 + mask_color3
   
    #res = cv2.bitwise_and(frame,frame, mask= mask)
    #edge = cv2.Canny(res,100,200)
    kernel = np.ones((1,1),None)
    kernel2 = np.ones((25,25),None)
    opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE, kernel2)

    cnt = cv2.findContours(closing,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnt)
    center = None
    X1 = 320
    radius = 1
    cnt
    if len(cnts)>0:

        c = max(cnts, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        try:
            
            X1 = int(M["m10"] / M["m00"])
            Y1 = int(M["m01"] / M["m00"])
            center = (X1, Y1)
        except Exception:
            print("divide by zero")
        if radius > 2:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0,0,255), -1)
    if len(cnts) > 0:
        Cone_Center = (X1)-320
        Cone_Center_2 = Cone_Center/320
        Step_Size = (Cone_Center_2*15)
        Servo_Current = (Servo_Current - Step_Size)
        if Servo_Current < 0:
            Servo_Current = 0
        elif Servo_Current > 180:
            Servo_Current = 180
    else:
        Servo_Current += Sweep_Step_Size
        if Servo_Current > 165:
            Sweep_Step_Size *= (-1)
        elif Servo_Current < 16:
            Sweep_Step_Size *= (-1)
    #current_value = X2
    #output = pid(current_value)
    #Sig = output+90
    kit.servo[Servo_Channel].angle = Servo_Current
    kit.servo[8].angle = Servo_Current
    if len(cnts) > 0:
        if Servo_Current <= AOE + 90 and Servo_Current >= 90 - AOE:
            if radius > 100:
                bool = True
                GPIO.output(relayPIN, 1)
            else:
                bool = False
                GPIO.output(relayPIN, 0)
        else:
            GPIO.output(relayPIN, 0)
        
    #cv2.imshow('clean fix',closing)
    #cv2.imshow('clean', opening)
    #cv2.imshow('edge',edge)
    cv2.imshow('frame',frame)
    #print(radius)
    #print(bool)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #print(Sig)
    #print(output)
    #print(center)
    #print(Half)
    #print(current_value)
    print (len(cnts))
    print(Servo_Current)
    print(Sweep_Step_Size)
    #print(dimensions[1])
    #print(dimensions)
    #print(type(cap))
        
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        GPIO.output(relayPIN, 0)
        GPIO.cleanup()
        break

cv2.destroyAllWindows()
