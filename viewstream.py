import cv2
import threading
stream1 = None
isConnected = False
def connect():  
    print('connect')  
    global stream1 
    global isConnected
    stream1 = cv2.VideoCapture("http://192.168.8.107:8080/stream/video.mjpeg")
    if stream1.isOpened():
      print('setting is Connected')
      isConnected = True
    else:
        isConnected = False
        t=threading.Timer(5,connect)
        t.start()
        print('no read streamy. try againy')
        #raise NameError('Just a Dummy Exception, write your own')
        
        
connect()

def run_detection(frame):
  print('run object detection')  

#cap = cv2.VideoCapture("http://192.168.8.107:8080/stream/video.mjpeg")
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter('output.mp4',fourcc, 10, (640,480))
frameCount=0

while True:   
  if isConnected == False:
    continue  
  ret, frame = stream1.read()  
  if ret == True:
    if frameCount%10 == 0:
      frameCount = 0
      run_detection(frame) 
      #out.write(frame)       
    frameCount+=1    
    cv2.imshow('Video', frame)     
    if cv2.waitKey(1) & 0xFF == ord('q'):
          break
  else:
    print('broken pipe, reconnect')
    isConnected = False    
    stream1.release()
    out.release()
    cv2.destroyAllWindows()
    t=threading.Timer(5,connect)
    t.start()
print('cap broken')    
stream1.release()
out.release()
cv2.destroyAllWindows()

