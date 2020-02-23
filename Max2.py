import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(-1)

while(1):

    # Take each frame
    _, frame = cap.read()


    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


 
    lower_value1 = np.array([110,160,100])
    upper_value1 = np.array([180,255,200])


    mask_color1 = cv2.inRange(hsv, lower_value1, upper_value1)
    mask = mask_color1
   
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
            cv2.circle(frame, (int(x), int(y)), int(radius),
            (0, 255, 255), 2)
            cv2.circle(frame, center, 10, (255, 0, 255), -3)
            cv2.circle(frame, (int(x2), int(y2)), int(radius2),
            (0, 255, 255), 2)
            cv2.circle(frame, center2, 10, (255, 0, 255), -3)

    cv2.imshow('clean fix',closing)
    #cv2.imshow('clean', opening)
   # cv2.imshow('edge',edge)
    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #print(center)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
