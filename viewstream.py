import cv2
import threading
import json

with open('config.json') as file:
  config = json.load(file)

urls = config['urls']
object_detection_interval = config['object_detection_interval']
stream_connect_retry_interval= config['stream_connect_retry_interval']
show_preview = config['show_preview']
streams = []
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter('output.mp4',fourcc, 10, (640,480))
frameCount=0

for url in config['urls']:
  streams.append({'cap' : None, 'url' : url})

def setStream(i):  
  active_stream = streams[i]  
  active_stream ['cap'] = cv2.VideoCapture(active_stream['url'])

def isStreamOpen(i):  
  if (streams[i]['cap'] == None):
     return False 
  return streams[i]['cap'].isOpened()

def connect(i):  
    print('connect')      
    setStream(i)
    if not isStreamOpen(i):                     
      print("Unable to read stream from camera at url: {}. Trying again in 5 seconds".format(streams[i]['url']))      
      t=threading.Timer(stream_connect_retry_interval,connect, [i])
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
    if show_preview: cv2.imshow(streams[0]['url'], frame)     
    if cv2.waitKey(1) & 0xFF == ord('q'):
          break
  else:
    print('broken pipe, reconnect')      
    active_stream.release()
    out.release()
    cv2.destroyAllWindows()
    t=threading.Timer(stream_connect_retry_interval, connect,[0])
    t.start()
print('cap broken')    
active_stream.release()
out.release()
cv2.destroyAllWindows()

