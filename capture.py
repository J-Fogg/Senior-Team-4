import cv2
import numpy as np
import imutils
import time
import board
import busio
import RPi.GPIO as GPIO
from imutils.video import VideoStream
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)     
relayPIN = 23                   # selects the gpio pin for the relay
GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPIN, GPIO.OUT)


cap = VideoStream(src=-1).start()    # starts the video stream

Servo_Current = 90                   # constants for the program
AOE = 20
Max_Step_Size = 6
Servo_Channel = 7
Sweep_Step_Size = Max_Step_Size
kit.servo[Servo_Channel].angle = 90

while(1):
    frame = cap.read()              # reads the frames
    dimensions = frame.shape        # gets the size of the frame

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    
 
    lower_value1 = np.array([157,184,180])         #sets the ranges for the color of the fire 
    upper_value1 = np.array([192,225,218])

    lower_value3 = np.array([157,184,180])
    upper_value3 = np.array([192,225,218])


    mask_color1 = cv2.inRange(hsv, lower_value1, upper_value1) # creates a binary image showing only the colors in range
    mask_color3 = cv2.inRange(hsv, lower_value3, upper_value3)
    mask = mask_color1 + mask_color3                            # combines the 2 binary images to one
   
    kernel = np.ones((1,1),None)                                # refines the image
    kernel2 = np.ones((25,25),None)
    opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE, kernel2)

    cnt = cv2.findContours(closing,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)   # gets the contours 
    cnts = imutils.grab_contours(cnt)
    center = None
    X1 = 320
    radius = 1

    if len(cnts)>0:         #  checks to see if there are contours 

        c = max(cnts, key=cv2.contourArea)              # gets the largest contour
        ((x,y), radius) = cv2.minEnclosingCircle(c)     # draws a circle around it 
        M = cv2.moments(c)
        try:
            
            X1 = int(M["m10"] / M["m00"])               # gets the center 
            Y1 = int(M["m01"] / M["m00"])
            center = (X1, Y1)
        except Exception:
            print("divide by zero")
        if radius > 2:                                  # if the radius is greater then 2 put a dot on the center 
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)  
            cv2.circle(frame, center, 5, (0,0,255), -1)
    if len(cnts) > 0:                       # checks if there is any contours
        Cone_Center = (X1)-320
        Cone_Center_2 = Cone_Center/320
        Step_Size = (Cone_Center_2*15)      # scales the step size of the servo
        Servo_Current = (Servo_Current - Step_Size)
        if Servo_Current < 0:               # makes sure servo stays in range 
            Servo_Current = 0
        elif Servo_Current > 180:
            Servo_Current = 180
    else:
        Servo_Current += Sweep_Step_Size        #sweeps of there is not contours 
        if Servo_Current > 165:
            Sweep_Step_Size *= (-1)
        elif Servo_Current < 16:
            Sweep_Step_Size *= (-1)

    kit.servo[7].angle = Servo_Current          # checks if the fire is on the correct side of the car
    if len(cnts) > 0:
        if Servo_Current <= AOE + 90 and Servo_Current >= 90 - AOE:
            if radius > 100:                    # checks to see of the fire is in range 
                bool = True
                GPIO.output(relayPIN, 1)
            else:
                bool = False
                GPIO.output(relayPIN, 0)
        else:
            GPIO.output(relayPIN, 0)

    cv2.imshow('frame',frame)
    print (Servo_Current)

        
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        GPIO.output(relayPIN, 0)
        GPIO.cleanup()
        break

cv2.destroyAllWindows()
