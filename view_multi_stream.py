from camera_display import CameraDisplay
import cv2
import sys
from streaming_camera import StreamingCamera
import json

with open('config.json') as file:
  config = json.load(file)

streams = []
#displays = []
for i, camera in enumerate(config['cameras']):
    url = camera['url']
    name = camera['name']
    stream_connect_retry_interval = config['stream_connect_retry_interval']
    streams.append(StreamingCamera(url, name, stream_connect_retry_interval))
    #displays.append(CameraDisplay(name))
  
while True:
    for i, stream in enumerate(streams):
        if stream.capture == None or stream.capture.isOpened() is False:
            continue
        if stream.frame_capture_successful != True:
            stream.reconnect()
            continue
        frame = stream.frame
        cv2.imshow(stream.name, stream.frame)
        #displays[i].frame = frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            for stream in streams:
                stream.capture.release()
                cv2.destroyAllWindows()
                sys.exit()
                break

