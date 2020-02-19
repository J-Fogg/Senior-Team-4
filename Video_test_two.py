import numpy as np
import cv2
import imutils

cap = cv2.VideoCapture('Pan Fire Video.MOV')

while(cap.isOpened()):
    ret, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


 
    lower_value1 = np.array([5,121,210])
    upper_value1 = np.array([25,171,255])

    lower_value3 = np.array([0,164,133])   
    upper_value3 = np.array([30,255,255])


    mask_color1 = cv2.inRange(hsv, lower_value1, upper_value1)
    mask_color3 = cv2.inRange(hsv, lower_value3, upper_value3)
    mask = mask_color1 + mask_color3
   
    res = cv2.bitwise_and(frame,frame, mask= mask)
    edge = cv2.Canny(res,100,200)
    kernel = np.ones((10,10),None)
    kernel2 = np.ones((10,10),None)
    opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE, kernel2)

    cnt = cv2.findContours(closing,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnt)
    for c in cnts:
	    M = cv2.moments(c)
	    cX = int(M["m10"] / M["m00"])
	    cY = int(M["m01"] / M["m00"])
	    cv2.drawContours(frame, [c], -1, (0, 255, 255), 2)
	    cv2.circle(frame, (cX, cY), 7, (255, 0, 255), -1)

    cv2.imshow('frame',frame)
    cv2.imshow('frame2',res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()