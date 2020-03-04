from queue import Queue
import cv2
import imutils
import numpy as np
import time
import threading
import serial
import json
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
Servo_Channel = 7

ser = serial.Serial("/dev/ttyS0", 115200 )

lower_value1 = np.array([142,176,119])
upper_value1 = np.array([180,255,200])
frame_Queue = Queue(120)
stop = False


Point = 1
radius = 1
max_step_size = 15
sweep_step_size = 5
servo = 90
servo_channel = 7
kit.servo[servo_channel].angle = 90

cap = cv2.VideoCapture(-1)

def find_centers(frame,sorted_cnts):
    try:
        center = [None]*len(sorted_cnts)
        for i in range(0 , len(sorted_cnts) ):
            M = cv2.moments(sorted_cnts[i])
            center[i] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.line(frame, center[i], (center[i][0],center[i][1]- 75),(0, 255 , 255), (3))
        return center
    except ZeroDivisionError:
        return sorted_cnts[0][0]
        

def stream_frame():
    global stop
    while not stop:
        ret,frame = cap.read()
        frame = cv2.flip(frame, -1)
        frame_Queue.put(frame)


def read_frame():
    global stop, lower_value1, upper_value1,radius,dist
    while not stop:
        frame = frame_Queue.get()
        frame_Queue.task_done()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_color1 = cv2.inRange(hsv, lower_value1, upper_value1)
        mask = mask_color1
   
        kernel = np.ones((1,1),None)
        kernel2 = np.ones((15,15),None)
        opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE, kernel2)
        cnt = cv2.findContours(closing,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        sorted_cnts = sorted(cnt[0], key=cv2.contourArea, reverse=True)
        cnts = enumerate(sorted_cnts)
        print (list(cnts))
        #sorted_cntss = sorted(cnt, key=cv2.contourArea, reverse=True)
        centers = find_centers(frame, sorted_cnts)
        #(x,y),radius = cv2.minEnclosingCircle(cnts)

        if len(centers) > 1:
            #print (cnt[0][0])
            center_point = (int((centers[0][0] + centers[1][0])/2),int((centers[0][1] + centers[1][1])/2))
            cv2.line(frame, (centers[0][0],centers[0][1]), (centers[1][0],centers[1][1]), (255, 0, 0), (3))
            cv2.line(frame, (center_point[0],center_point[1]), (center_point[0],center_point[1]), (0, 255, 0), (10))
            dist = distance(radius)
            servo_control(center_point[0], dist)
            dist = distance(radius)
        else:
            sweep_search()
           # print("search")
            
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop = True
            break
        
def distance(radius):
    distance = (radius * 1.35)/2.54
    return (distance)



def servo_control(center_of_cones,dist):
    global servo
    max_step_size = 5
    center_scaled = (center_of_cones-320) # -320 to 320
    
    normalized_scale = (center_scaled)/320 # scale -1 to 1
    step_p = (normalized_scale* -max_step_size)
    #print(step_p , "step_p")
    if abs(step_p) > 0.5:
        servo += (step_p)
    if servo < 10:
        servo = 10
    elif servo > 170:
        servo = 170
    transmit(servo,center_of_cones, dist)
    kit.servo[servo_channel].angle = servo
    #print(servo)
    
def sweep_search():
    global servo, sweep_step_size
    servo += sweep_step_size
    if servo > 165:
        sweep_step_size *= (-1)
    elif servo < 16:
        sweep_step_size *= (-1)
    kit.servo[servo_channel].angle = servo

def transmit(servo,center_of_cones,dist ):
    correction = (servo + (-30/320)*(center_of_cones - 320))-90
    #tup1 = (correction, dist)
   # print(correction)
    #print(tup1)
    #print(center_of_cones)
    servo_json = json.dumps(correction)
    ser.write(servo_json.encode())
    ser.write('\r\n'.encode())
    print(servo_json)
    '''ser.write(','.encode())
    dist_json = json.dumps(dist)
    ser.write(dist_json.encode())
    print(dist_json)'''
        
    
def main():
    thread_stream = threading.Thread(target=stream_frame)
    thread_read = threading.Thread(target=read_frame)
    #thread_transmit = threading.Thread(target=transmit)
    #thread_servo = threading.Thread(target=servo_control)
    thread_stream.start()
    time.sleep(0.5)
    thread_read.start()
    #thread_transmit.start()
    #thread_servo.start()
    thread_stream.join()
    thread_read.join()
    #thread_transmit.join()
    #thread_servo.join()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()
