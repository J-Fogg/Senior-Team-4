import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()


    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


 
    lower_value1 = np.array([5,121,180])
    upper_value1 = np.array([50,210,255])

    lower_value3 = np.array([20,120,50])
    upper_value3 = np.array([200,255,170])


    mask_color1 = cv2.inRange(hsv, lower_value1, upper_value1)
    mask_color3 = cv2.inRange(hsv, lower_value3, upper_value3)
    mask = mask_color1 + mask_color3
   
    res = cv2.bitwise_and(frame,frame, mask= mask)
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
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0,0,255), -1)
    cv2.imshow('clean fix',closing)
    #cv2.imshow('clean', opening)
   # cv2.imshow('edge',edge)
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    print(center)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

