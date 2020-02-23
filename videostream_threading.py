from queue import Queue
import cv2
import imutils
from imutils.video import VideoStream
import time
import threading 

frame_Queue = Queue(120)
stop = False

cap = VideoStream(-1).start()


def stream_frame():
    global stop
    while not stop:
        frame = cap.read()
        frame_Queue.put(frame)

def read_frame():
    global stop
    while not stop:
        frame = frame_Queue.get()
        frame_Queue.task_done()
        cv2.imshow('frame', frame)
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


