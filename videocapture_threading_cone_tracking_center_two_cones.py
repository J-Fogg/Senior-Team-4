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
Servo_Channel = 7                           # Sets the channel of the pca9685 to 7

ser = serial.Serial("/dev/ttyS0", 115200 )  # Selects the port and baud rate for serial communications

lower_value1 = np.array([100,164,133])      # color values for the cones 
upper_value1 = np.array([180,255,233])
frame_Queue = Queue(120)                    # limits the queue 4 seconds of frames 
stop = False

radius = 1                                  # constants needed through out the program
max_step_size = 10
sweep_step_size = 4
servo = 90
servo_channel = 7
kit.servo[servo_channel].angle = 90

cap = cv2.VideoCapture(-1)                  # selects the correct capture mode and the camera to use 

def find_centers(frame,sorted_cnts):        
    try:
        center = [None]*len(sorted_cnts)    # gets the coordinates of the contours  
        for i in range(0 , len(sorted_cnts) ): # a for loop to find the centers and draw a circle on them 
            M = cv2.moments(sorted_cnts[i])
            center[i] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(frame, center[i],(3),(0, 200 , 200), (3))
            cv2.line(frame, center[i], (center[i][0],center[i][1]- 75),(0, 200 , 0), (3))
        return center
    except ZeroDivisionError:
        return sorted_cnts[0][0]
    
def find_distance (frame, contours):
    radius = None
    for i in range(0 , len(contours) ):
        center,radius = cv2.minEnclosingCircle(contours[i])
        cv2.circle(frame, (int(center[0]),int(center[1])),int(radius),(0, 200 , 200), (3))
    return radius

def stream_frame():                         # This definition captures the frames and places them in a queue
    global stop
    while not stop:
        ret,frame = cap.read()
        frame = cv2.flip(frame, -1)
        frame_Queue.put(frame)


def read_frame():
    global stop, lower_value1, upper_value1,radius
    while not stop:
        frame = frame_Queue.get()                              # gets frames from queue
        frame_Queue.task_done()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)           #converts them to HSV values
        mask = cv2.inRange(hsv, lower_value1, upper_value1)    # converts it to a binary image 
   
        kernel = np.ones((1,1),None)                           # refines the image
        opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN, kernel)
        kernel2 = np.ones((15,15),None)
        closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE, kernel2)
        
        cnt, circle_data = cv2.findContours(closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)    # finds the contours in the image
        sorted_cnts = sorted(cnt, key=cv2.contourArea, reverse=True)                            # sorts the contours from largest to smallest

        
        centers = find_centers(frame, sorted_cnts)             # sends them to the find_centers definition 
        if len(centers) > 1: 
            center_point = (int((centers[0][0] + centers[1][0])/2),int((centers[0][1] + centers[1][1])/2)) # finds the center of the two centers 
            cv2.line(frame, (centers[0][0],centers[0][1]), (centers[1][0],centers[1][1]), (255, 0, 0), (3))
            cv2.line(frame, (center_point[0],center_point[1]), (center_point[0],center_point[1]), (0, 255, 0), (10))
            servo_control(center_point[0], centers)             # send information to servo_control
        else:
            sweep_search()                                      # if no centers it sweeps 
            
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop = True
            break
        

def servo_control(center_of_cones, centers):            
    global servo
    max_step_size = 5
    center_scaled = (center_of_cones-320) # -320 to 320     # puts the pixal counts on a scale of -320 to 320, zero being center 
    
    normalized_scale = (center_scaled)/320 # scale -1 to 1  # scales it to be -1 to 1 with 0 still center
    step_p = (normalized_scale* -max_step_size)             
    if abs(step_p) > 0.5:
        servo += (step_p)
    if servo < 10:                          # keeps it in range
        servo = 10
    elif servo > 170:
        servo = 170
    transmit(servo, centers)
    kit.servo[servo_channel].angle = servo  # turns the servo 
    
def sweep_search():                         # just sweeps back and forth looing for cones 
    global servo, sweep_step_size
    servo += sweep_step_size
    if servo > 165:
        sweep_step_size *= (-1)
    elif servo < 16:
        sweep_step_size *= (-1)
    kit.servo[servo_channel].angle = servo

def transmit(servo, centers):
    correction = (-1*((servo + (-30/320)*(centers[0][0] - 320))-90)) , (-1*((servo + (-30/320)*(centers[1][0] - 320))-90)) # converts it to degrees
    servo_json = json.dumps(correction)     # packages it for transmitting 
    ser.write(servo_json.encode())      
    ser.write('\r\n'.encode())              # sends to navigation 
    
        
    
def main():
    thread_stream = threading.Thread(target=stream_frame) # threading.Thread is use to build the thread and point to the correct definition 
    thread_read = threading.Thread(target=read_frame)
    thread_stream.start()                                 # thread.start is used to actually start the thread
    time.sleep(0.5)                                       # short time delay to recieve the first frame
    thread_read.start()
    thread_stream.join()                                  # This closes the threads at the end 
    thread_read.join()
    cv2.destroyAllWindows()


if __name__=="__main__":                                 # runs the code in the correct order    
    main()
