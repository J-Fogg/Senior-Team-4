from queue import Queue
import cv2
import imutils
import numpy as np
from imutils.video import VideoStream
import time
import threading

frame_Queue = Queue(120)
stop = False

cap = cv2.VideoCapture(-1)

def find_centers(frame,sorted_cnts):
    try:
        center = [None]*len(sorted_cnts)
        for i in range(0 , len(sorted_cnts) ):
            #print(i)
            M = cv2.moments(sorted_cnts[i])
            center[i] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.line(frame, center[i], (center[i][0],center[i][1]- 75),(0, 255 , 255), (3))
        return center
    except ZeroDivisionError:
        #print('AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
        return sorted_cnts[0][0]
        


def stream_frame():
    global stop
    while not stop:
        ret,frame = cap.read()
        frame_Queue.put(frame)

def read_frame():
    global stop
    while not stop:
        frame = frame_Queue.get()
        frame_Queue.task_done()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        lower_value1 = np.array([142,176,119])
        upper_value1 = np.array([180,255,200])


        mask_color1 = cv2.inRange(hsv, lower_value1, upper_value1)
        mask = mask_color1
   
        kernel = np.ones((1,1),None)
        kernel2 = np.ones((15,15),None)
        opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE, kernel2)
        cnt = cv2.findContours(closing,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        sorted_cnts = sorted(cnt[0], key=cv2.contourArea, reverse=True)#[:]
        #print(sorted_cnts[0])
        centers = find_centers(frame, sorted_cnts)
        #print(centers)
        if len(centers) > 1: 
            center_point = (int((centers[0][0] + centers[1][0])/2),int((centers[0][1] + centers[1][1])/2))
            cv2.line(frame, (centers[0][0],centers[0][1]), (centers[1][0],centers[1][1]), (255, 0, 0), (3))
            cv2.line(frame, (center_point[0],center_point[1]), (center_point[0],center_point[1]), (0, 255, 0), (10))
            #cnts = imutils.grab_contours(cnt) # equals cnt[0]
        try:
            #if len(cnt) > 0:
                #((x, y), radius) = cv2.minEnclosingCircle(D[0])
                #((x2, y2), radius2) = cv2.minEnclosingCircle(D[1])
                #M = cv2.moments(D[0])
                #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                #M2 = cv2.moments(D[1])
                #center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))
                #center3 = (int((center[0] + center2[0])/2),int((center[1] + center2[1])/2))
                #print(cnt[0][0])
                #if radius > 10:
                    #cv2.circle(frame, (int(x), int(y)), int(radius),
                    #(0, 255, 255), 2)
                    #cv2.circle(frame, center, 10, (255, 0, 255), -3)
                    #cv2.circle(frame, (int(x2), int(y2)), int(radius2),
                    #(0, 255, 255), 2)
                    #cv2.circle(frame, center2, 10, (255, 0, 255), -3)
                #cv2.line(frame, center, (center[0],center[1]- 75),(0, 0, 255), (3))
                #cv2.line(frame, center2, (center2[0],center2[1]- 75),(255, 0, 0), (3))
                #cv2.line(frame, (center[0],center[1]), (center2[0],center2[1]), (0, 255, 0), (3))
                #cv2.line(frame, (center3[0],center3[1]), (center3[0],center3[1]), (255, 255, 255), (10))
                i = 0
                for i in range(0 , len(D) ):
                    for j in range(0 , len(D[i])):
                        #print(i,len(D[i]))
                        #print(D[i][j][0][0],D[i][j][0][1]) # [contour number][points][0][component]
                        cv2.circle(frame, (int(D[i][j][0][0]),int(D[i][j][0][1])), 1, (0, 255, 255), 2)
                    #i += 1
                    #print(i)
                    
                    
                #print('HIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
                
        except Exception:
            pass
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop = True
            break
    
    
def main():
        thread_stream = threading.Thread(target=stream_frame)
        thread_read = threading.Thread(target=read_frame)
        thread_stream.start()
        time.sleep(0.5)
        thread_read.start()
        thread_stream.join()
        thread_read.join()




if __name__=="__main__":
    main()

cv2.destroyAllWindows()




