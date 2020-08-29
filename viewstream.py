import cv2
cap = cv2.VideoCapture("http://192.168.8.107:8080/stream/video.mjpeg")
print(type(cap))
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = cv2.VideoWriter('output.mp4',fourcc, 10, (640,480))
frameCount=0
isStreaming = True
while True:
  ret, frame = cap.read()  
  if ret == True:
    # if frameCount%10 == 0:
    #   frameCount = 0 
    #   out.write(frame)       
    # frameCount+=1    
    cv2.imshow('Video', frame)  
    #out.write(frame)   
    if cv2.waitKey(1) & 0xFF == ord('q'):
          break
  else:
    print('broken pipe')
    print(cap)
    isStreaming = False
print('cap broken')    
cap.release()
out.release()
cv2.destroyAllWindows()
