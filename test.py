import cv2
import imutils
import numpy as np
import matplotlib
img = cv2.imread('IMG_7298sm.jpg',1)
dim = (172, 300)
img2 = cv2.resize(img, dim)
img5 = img2
while (1):
    hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
    lower_value1 = np.array([5,121,210])
    upper_value1 = np.array([25,171,255])

    lower_value3 = np.array([0,164,133])   
    upper_value3 = np.array([30,255,255])


    mask_color1 = cv2.inRange(hsv, lower_value1, upper_value1)
    mask_color3 = cv2.inRange(hsv, lower_value3, upper_value3)
    mask = mask_color1 + mask_color3
    res = cv2.bitwise_and(img2,img2, mask= mask)
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(contours)
   # M = cv2.moments(cnt)
   # cx = int(M['m10']/M['m00'])
    #cy = int(M['m01']/M['m00'])
    #show = cv2.convexHull(cnts[-1])

   # cnts = []
   #while(c < 5)
      #  x,y,w,h = cv2.boundingRect(cnts[0])
      #  cv2.rectangle(img5,(x,y),(x+w,y+h),(0,255,0),2)
        
    #   cv2.drawContours(mask,cnts,-1,(0,255,0),3)
    cv2.imshow('IMG_7298sm.jpg', img2)
    cv2.imshow("mask", mask) 
    cv2.imshow("bitwise", res)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
