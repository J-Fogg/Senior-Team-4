from queue import Queue
import cv2
import imutils
from imutils.video import VideoStream
import time
q = Queue()

def stream_frame():
    pi
    frame = cap.read()
    q.put(frame)

def read_frame():
    frame = q.get()
    q.task_done()
    cv2.imshow('frame', frame)

    
def main():
    while True:
        cap = VideoStream(src=-1).start()
        frame = cap.read()
        cv2.imshow('frame', frame)





if __name__=="__main__":
    main()

cv2.destroyAllWindows()

