import cv2
import threading
import json

with open('config.json') as file:
  config = json.load(file)

urls = config['urls'] # camera urls
run_object_detection_every_n_frames = config['run_object_detection_every_n_frames'] #
stream_connect_retry_interval= config['stream_connect_retry_interval']
show_preview = config['show_preview']
streams = []
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter('output.mp4',fourcc, 10, (640,480))
frameCount=0

for url in config['urls']:
  print('create stream')
  streams.append({'cap' : None, 'url' : url})

def setStream(i):  
  stream = streams[i]  
  stream['cap'] = cv2.VideoCapture(stream['url'])  

def isStreamOpen(i):  
  if (streams[i]['cap'] == None): 
    return False 
  return streams[i]['cap'].isOpened()

def connect(i):  
    print('connect')      
    setStream(i)
    if not isStreamOpen(i):                     
      print("Unable to read stream from camera at url: {}. Trying again in 5 seconds".format(streams[i]['url']))      
      threading.Timer(stream_connect_retry_interval,connect, [i]).start()
      

def reconnect(stream):
  print('Unable to stream from {}. Attempting to reconnect'.format(stream["url"]))  
  stream["cap"] = None          
  t=threading.Timer(stream_connect_retry_interval, connect,[0])
  t.start()

for i, stream in enumerate(streams):
  connect(i)

while True:
  i = 0
  for i, stream in enumerate(streams):          
    if not isStreamOpen(i):      
      continue    
    frame_capture_successful, frame = stream["cap"].read()
    if frame_capture_successful != True:
      reconnect(stream)
      continue
    #if frameCount%3 == 0:
    #  frameCount = 0                  
    cv2.imshow(str(i), frame)          
    #   #out.write(frame)      
    #frameCount+=1   
    
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
      
print('Ending Nightwatch service.')    
streams[0]['cap'].release() #iterate over all
out.release()
cv2.destroyAllWindows()

