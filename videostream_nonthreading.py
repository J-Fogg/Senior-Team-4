from queue import Queue
import cv2
import imutils
from imutils.video import VideoStream
import time
import threading 

frame_Queue = Queue()
stop = False

cap = VideoStream(-1).start()


def stream_frame():
        frame = cap.read()
        frame_Queue.put(frame)

def read_frame():
        frame = frame_Queue.get()
        frame_Queue.task_done()
        cv2.imshow('frame', frame)

    
def main():
    global stop
    while not stop:
        stream_frame()
        read_frame()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop = True
            break




if __name__=="__main__":
    main()

cv2.destroyAllWindows()
cap.release


