import cv2
import numpy as np
import imutils
while(1):
    img = cv2.imread('IMG_7298sm.jpg',1)
    dim = (600, 480)
    img2 = cv2.resize(img, dim)

cv2.imshow('IMG_7298sm.jpg', img2)
key = cv2.waitKey(1) & 0xFF