from camera_display import CameraDisplay
import cv2, time, json, sys
from streaming_camera import StreamingCamera
from multiprocessing import Process, Queue

process_is_alive = True

def detect_object(net, input_queue, output_queue):
    while process_is_alive == True:
        if not input_queue.empty():
            [camera, frame] = input_queue.get()            
            #detections = engine.detect_with_image(frame)
            detections = ''
            output_queue.put([camera, detections])
            time.sleep(0.01)        

def goodbye():
    global process_is_alive
    process_is_alive = False
    for stream in streams:
        stream.capture.release()
        stream.is_alive = False
    cv2.destroyAllWindows()        
    print('Goodbye')    
    exit(1)

if __name__ == '__main__':
    engine = 'GET ENGINE'    

    detection_input_queue = Queue()
    detection_output_queue = Queue()
    detections = None

    with open('config.json') as file:
        config = json.load(file)

    streams = []

    for i, camera in enumerate(config['cameras']):
        url = camera['url']
        name = camera['name']
        stream_connect_retry_interval = config['stream_connect_retry_interval']
        streams.append(StreamingCamera(url, name, stream_connect_retry_interval))

    p = Process(target=detect_object, args=(engine, detection_input_queue,
                                            detection_output_queue,))
    p.daemon = True
    p.start()

    while True:
        for i, stream in enumerate(streams):
            if stream.capture == None or stream.capture.isOpened() is False:
                continue
            if stream.frame_capture_successful != True:
                stream.reconnect()
                continue
            frame = stream.frame
            detection_input_queue.put(['camera',frame])
            if not detection_output_queue.empty():
                [camera, detections] = detection_output_queue.get()
            cv2.imshow(stream.name, stream.frame)                       
            if cv2.waitKey(1) & 0xFF == ord('q'):
                process_is_alive = False
                for stream in streams:
                    stream.capture.release()
                    stream.is_alive = False
                cv2.destroyAllWindows()
                time.sleep(2) 
                for stream in streams:
                    stream.capture.release()
                    stream.thread.join()       
                print('Goodbye')    
                exit(1)        
                