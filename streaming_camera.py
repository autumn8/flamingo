from threading import Thread, Timer
import cv2, time, sys


class StreamingCamera(object):
    def __init__(self, url, name, stream_connect_retry_interval):
        self.frame_capture_successful = False
        self.stream_connect_retry_interval = stream_connect_retry_interval
        self.url = url 
        self.is_alive = True
        self.name = name     
        self.capture = cv2.VideoCapture(self.url)  
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start() 
        self.connect()        

    def connect(self):
        print("Connecting to {} at {}".format(self.name, self.url))
        self.capture = cv2.VideoCapture(self.url)
        if self.capture == None or self.capture.isOpened() is False:                    
            print("Unable to read stream from camera at url: {}. Trying again in 5 seconds".format(self.url))      
            Timer(self.stream_connect_retry_interval, self.connect).start()
         

    def update(self):        
        while self.is_alive == True:   
            if self.capture == None or self.capture.isOpened() is False:     
                continue        
            (self.frame_capture_successful, self.frame) = self.capture.read()
            time.sleep(0.01)
        print("Closing stream for {}".format(self.name))            
        self.capture = None
        cv2.destroyWindow(self.name)

    def reconnect(self):        
        print('Unable to stream from {}. Attempting to reconnect'.format(self.url))  
        self.capture = None                 
        Timer(self.stream_connect_retry_interval, self.connect).start()   

    