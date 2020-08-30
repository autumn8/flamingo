from threading import Thread, Timer
import cv2, time
import sys

class StreamingCamera(object):
    def __init__(self, url, name, stream_connect_retry_interval):
        self.frame_capture_successful = False
        self.stream_connect_retry_interval = stream_connect_retry_interval
        self.url = url 
        self.name = name     
        self.capture = cv2.VideoCapture(self.url)  
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start() 
        self.connect()        

    def connect(self):
        self.capture = cv2.VideoCapture(self.url)
        if self.capture == None or self.capture.isOpened() is False:                    
            print("Unable to read stream from camera at url: {}. Trying again in 5 seconds".format(self.url))      
            Timer(self.stream_connect_retry_interval, self.connect).start()
         

    def update(self):        
        while True:   
            if self.capture == None or self.capture.isOpened() is False:     
                continue        
            (self.frame_capture_successful, self.frame) = self.capture.read()
            time.sleep(0.05)

    def reconnect(self):        
        print('Unable to stream from {}. Attempting to reconnect'.format(self.url))  
        self.capture = None                 
        Timer(self.stream_connect_retry_interval, self.connect).start()

    