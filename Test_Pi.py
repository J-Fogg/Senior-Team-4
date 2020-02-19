# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import imutils
import time
import cv2
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size =(640, 480) )
 
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

    lower_value3 = np.array([100,164,120])   
    upper_value3 = np.array([200,255,255])



    mask_color1 = cv2.inRange(hsv, lower_value1, upper_value1)
    mask_color3 = cv2.inRange(hsv, lower_value3, upper_value3)
    mask = mask_color1 + mask_color3
   
    #res = cv2.bitwise_and(image,image, mask= mask)
    #edge = cv2.Canny(res,100,200)
    kernel = np.ones((10,10),None)
    kernel2 = np.ones((10,10),None)
    opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE, kernel2)

    cnt = cv2.findContours(closing,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnt)
    if len(cnts) > 1:
        D = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
        ((x, y), radius) = cv2.minEnclosingCircle(D[0])
        ((x2, y2), radius2) = cv2.minEnclosingCircle(D[1])
        M = cv2.moments(D[0])
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        M2 = cv2.moments(D[1])
        center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))
        print(D[1])
        if radius > 10:
            cv2.circle(image, (int(x), int(y)), int(radius),
            (0, 255, 255), 2)
            cv2.circle(image, center, 10, (255, 0, 255), -3)
            cv2.circle(image, (int(x2), int(y2)), int(radius2),
            (0, 255, 255), 2)
            cv2.circle(image, center2, 10, (255, 0, 255), -3)

    cv2.imshow('clean fix',closing)
    #cv2.imshow('clean', opening)
   # cv2.imshow('edge',edge)
    cv2.imshow('frame',image)
    cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #print(center)
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
 
    # if the `q` key was pressed, break from the loop