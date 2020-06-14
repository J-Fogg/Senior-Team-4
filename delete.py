# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import imutils
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
     
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower_value1 = np.array([5,121,210])
    upper_value1 = np.array([25,171,255])

    lower_value3 = np.array([0,164,133])
    upper_value3 = np.array([30,255,255])
    
    mask_color1 = cv2.inRange(hsv, lower_value1, upper_value1)
    mask_color3 = cv2.inRange(hsv, lower_value3, upper_value3)
    mask = mask_color1 + mask_color3
    
    res = cv2.bitwise_and(image,image, mask= mask)
    edge = cv2.Canny(res,100,200)
    kernel = np.ones((10,10),None)
    kernel2 = np.ones((25,25),None)
    opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE, kernel2)
    
    cnt = cv2.findContours(closing,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnt)
    center = None
    if len(cnts)>0:

        c = max(cnts, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 2:
            cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(image, center, 5, (0,0,255), -1)
    
    
    #cv2.imshow('clean fix',closing)
    #cv2.imshow('clean', opening)
    #cv2.imshow('edge',edge)
    #cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    print(center)
    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
 
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
 
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break