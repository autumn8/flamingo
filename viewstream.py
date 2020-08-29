import cv2
import threading
connection_retry_interval = 5
urls = ["http://192.168.8.107:8080/stream/video.mjpeg"]
streams = []
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter('output.mp4',fourcc, 10, (640,480))
frameCount=0

for url in urls:
  streams.append({'cap' : None, 'url' : url})

def setStream(i):
  print(cv2)
  #globals()['stream' + str(i)] = cv2.videoCapture(url)
  active_stream = streams[i]
  print(active_stream['cap'])
  print(active_stream['url'])
  active_stream ['cap'] = cv2.VideoCapture(active_stream['url'])

def isStreamOpen(i):
  #return globals()['stream' + str(i)].isOpened() 
  if (streams[i]['cap'] == None):
     return False 
  return streams[i]['cap'].isOpened()

def connect(i):  
    print('connect')      
    setStream(i)
    if not isStreamOpen(i):                     
      print("Unable to read stream. Trying again in 5 seconds")      
      t=threading.Timer(connection_retry_interval,connect, [i])
      t.start()        
        
connect(0)

while True:   
  if not isStreamOpen(0):
    continue
  active_stream = streams[0]['cap']  
  ret, frame = active_stream.read()  
  if ret == True:
    if frameCount%10 == 0:
      frameCount = 0      
      #out.write(frame)       
    frameCount+=1    
    cv2.imshow('Video', frame)     
    if cv2.waitKey(1) & 0xFF == ord('q'):
          break
  else:
    print('broken pipe, reconnect')      
    active_stream.release()
    out.release()
    cv2.destroyAllWindows()
    t=threading.Timer(5,connect,[0])
    t.start()
print('cap broken')    
active_stream.release()
out.release()
cv2.destroyAllWindows()

