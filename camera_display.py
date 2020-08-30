from threading import Thread, Timer
import cv2, time
import sys

class CameraDisplay(object):
    def __init__(self, name):
        print('init')
        self.name = name
        self.frame = None
        self.stopped = False
        self.thread = Thread(target=self.show, args=()).start()        
        

    def show(self):        
        while not self.stopped:            
            if self.frame is not None:
                cv2.imshow(self.name, self.frame)
                self.frame = None            

    def stop(self):
        cv2.destroyWindow(self.name)
        self.stopped = True