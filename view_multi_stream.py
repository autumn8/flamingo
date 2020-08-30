from streaming_camera import StreamingCamera
import json

with open('config.json') as file:
  config = json.load(file)

streams = []
for i, camera in enumerate(config['cameras']):
    url = camera['url']
    name = camera['name']
    stream_connect_retry_interval = config['stream_connect_retry_interval']
    streams.append(StreamingCamera(url, name, stream_connect_retry_interval))
  
while True:
    for stream in streams:
        stream.show_frame()