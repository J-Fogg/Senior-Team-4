# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import math
import time
import board
import busio
import RPi.GPIO as GPIO
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
hat = adafruit_pca9685.PCA9685(i2c)
hat.frequency = 60




# construct the argument parse and parse the arguments

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help='pan.avi')
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
#GPIO.output(26, GPIO.HIGH)
GPIO.setup(21, GPIO.OUT)
#GPIO.output(21, GPIO.HIGH)
GPIO.setup(20, GPIO.OUT)
#GPIO.output(20, GPIO.HIGH)
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (150,150,0)
greenUpper = (250,360,360)
#pts = deque(maxlen=args["buffer"])
bottommost = []
C = []
CNTS = []
kit.servo[1].angle = 90
degree = 90
i = 89

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    vs = VideoStream(src=-1).start()
    

# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])
#args["video"]
# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
    # grab the current frame
    frame = vs.read()

    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "orange", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=10)
    mask = cv2.dilate(mask, None, iterations=10)

    # find contours in the mask and initialize the current
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
      

    if  len(cnts) < 1:
        i += 3
        kit.servo[1].angle = i
        time.sleep(0.0001)
        if (i > 150):
            i = 0
        
    # only proceed if at least 2 contour were found
    
    if len(cnts) > 0 :
        #cont = cnts[0]
        # find the 2 largest contours in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        
        D = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
        cont = D[0]
        contt = np.squeeze(D[0])
        ((x, y), radius) = cv2.minEnclosingCircle(D[0])
        #((x2, y2), radius2) = cv2.minEnclosingCircle(D[1])
        M = cv2.moments(D[0])
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        CenterX = center[0]
        CenterY = center[0]
        #M2 = cv2.moments(D[1])
        #center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))
        #if center[0] < center2[0]:
            #CenterX = ((center2[0] - center[0])/2) + center[0]
        #if center[0] > center2[0]:
            #CenterX = ((center[0] - center2[0])/2) + center2[0]
        #if center[1] < center2[1]:
            #CenterY = ((center2[1] - center[1])/2) + center[1]
        #if center[1] > center2[1]:
            #CenterY = ((center2[1] - center[1])/2) + center2[1]
        if (CenterX < 270):
            GPIO.output(21,GPIO.HIGH)
            GPIO.output(20,GPIO.LOW)
            Turn = 0
            Straight = 1
            degree= (320 - CenterX)/15 + degree
            
            if degree > 150:
                degree = 150
                
        if CenterX > 330:
            GPIO.output(21,GPIO.LOW)
            GPIO.output(20,GPIO.LOW)
            Turn = 1
            Straight = 1
            degree= degree - (CenterX - 320)/15
            
            if degree < 10:
                degree = 10
        if (CenterX > 270) & (CenterX < 330):
            GPIO.output(20,GPIO.HIGH)
            Straight = 0
        degree = kit.servo[1].angle = degree
        lastdegree = degree
        MaxY = sorted(contt, key=lambda x: x[1], reverse=True)[:50]
        LeftX = sorted(MaxY, key=lambda x: x[0])
        RightX = sorted(MaxY, key=lambda x: x[0], reverse=True)
        Middle = int((RightX[0][0]-LeftX[0][0])/2 + LeftX[0][0])
        Object = (428*14.5)/(RightX[0][0]-LeftX[0][0])
        print(Object, Straight, Turn, CenterX)
        if (Object < 50):
            GPIO.output(26,GPIO.LOW)
        if (Object > 50):
            GPIO.output(26,GPIO.HIGH)
        #GPIO.cleanup()
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (255, 255, 255), 2)
            cv2.circle(frame, center, 10, (0, 0, 0), -3)
            #cv2.circle(frame, (int(x2), int(y2)), int(radius2),
                #(255, 255, 255), 2)
            cv2.circle(frame, (int(CenterX),int(CenterY)), 15,(255, 255, 255), 2)
            cv2.circle(frame, (Middle, LeftX[0][1]), 10,(255, 255, 255), 2)
            #cv2.circle(frame, center2, 10, (0, 0, 0), -3)
    
        
         
            
    # update the points queue
    #pts.appendleft(center)


    # show the frame to our screen
    cv2.imshow("Frame", frame)
    cv2.imshow("Frame2", mask)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera
else:
    vs.release()

# close all windows
cv2.destroyAllWindows()
