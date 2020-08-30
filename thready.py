from threading import Thread
import cv2, time

class VideoStreamWidget(object):
    def __init__(self, src, name):
        self.capture = cv2.VideoCapture(src)
        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.name = name

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            time.sleep(.01)

    def show_frame(self):
        # Display frames in main program
        cv2.imshow(self.name, self.frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            exit(1)

if __name__ == '__main__':
    video_stream_widget0 = VideoStreamWidget("http://192.168.8.107:8080/stream/video.mjpeg", 'fron')
    video_stream_widget1 = VideoStreamWidget("http://192.168.8.220:8080/stream/video.mjpeg", 'garden')
    video_stream_widget2 = VideoStreamWidget("http://192.168.8.107:8080/stream/video.mjpeg", 'fronfasdf')
    video_stream_widget3 = VideoStreamWidget("http://192.168.8.220:8080/stream/video.mjpeg", 'gardenwerwe')
    while True:
        try:
            video_stream_widget0.show_frame()
            video_stream_widget1.show_frame()
            video_stream_widget2.show_frame()
            video_stream_widget3.show_frame()
        except AttributeError:
            pass