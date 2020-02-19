import cv2
import numpy as np
import argparse
import imutils


lowerBound = np.array([0,150,150])
upperBound = np.array([250,360,360])

cam= cv2.VideoCapture('pan.avi')
kernelOpen=np.ones((5,5))
kernelClose=np.ones((60,60))
OldBig = 0
contsSorted = []
oldA = 0
CS = []
My_List = []
Bot = []
while (1):

    ret, img =cam.read()
   
    

    #convert BGR to HSV
    imgHSV= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

    maskFinal=maskClose
    maskFinal = cv2.erode(maskFinal, None, iterations=5)
    maskFinal = cv2.dilate(maskFinal, None, iterations=5)
    _,conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    Num = 0
    areaArray = []
    cv2.drawContours(img,conts,-1,(255,0,0),3)
    
    for i in range(len(conts)):
        
        x,y,w,h=cv2.boundingRect(conts[i])
        II = y + h
        Hate = [x,II]
    
                
        ret,thresh = cv2.threshold(mask,250,255,0)
        Rect = cv2.minAreaRect(conts[i])
        box = cv2.boxPoints(Rect)
        box = np.int0(box)
        
        img = cv2.drawContours(img,[box], 0, (0,0,255),2)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
        K = int(y+h)
        for i, c in enumerate(conts):
            area = cv2.contourArea(c)
            areaArray.append(area)
        c = max(conts, key=cv2.contourArea)
        contsSorted = sorted(conts, key=lambda x: cv2.contourArea(x), reverse = True)[:2]
        CS.append(contsSorted)
        M1 = cv2.moments(contsSorted[i])    
        cXX = int(M1["m10"] / M1["m00"])
        cYY = int(M1["m01"] / M1["m00"])    
        cv2.circle(img, (cXX, cYY), 5, (200, 255, 255), -1)
        print(contsSorted)
        (A,B), (MA,ma), angle = cv2.fitEllipse(conts[i])
        I = int(2*i)
        res = conts[i]
        res1 = list(map(max, zip(res))) 
        res2 = list(map(min, zip(res)))  
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        if angle < 90 :
            Center = int(x + w)
        if angle > 90 :
            HHH = 1

    cv2.imshow("cam",img)
    cv2.waitKey(10)