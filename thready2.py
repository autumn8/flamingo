import threading
import cv2



class VideoGetter():
    def __init__(self, src):
        """
        Class to read frames from a VideoCapture in a dedicated thread.
        Args:
            src (int|str): Video source. Int if webcam id, str if path to file.
        """
        self.cap = cv2.VideoCapture(src)
        self.grabbed, self.frame = self.cap.read()
        self.stopped = False

    def start(self):
        threading.Thread(target=self.get, args=()).start()
        return self

    def get(self):
        """
        Method called in a thread to continually read frames from `self.cap`.
        This way, a frame is always ready to be read. Frames are not queued;
        if a frame is not read before `get()` reads a new frame, previous
        frame is overwritten.
        """
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                self.grabbed, self.frame = self.cap.read()

    def stop(self):
        self.stopped = True


class VideoShower():
    def __init__(self, frame=None, win_name="Video"):
        """
        Class to show frames in a dedicated thread.
        Args:
            frame (np.ndarray): (Initial) frame to display.
            win_name (str): Name of `cv2.imshow()` window.
        """
        self.frame = frame
        self.win_name = win_name
        self.stopped = False

    def start(self):
        threading.Thread(target=self.show, args=()).start()
        return self

    def show(self):
        """
        Method called within thread to show new frames.
        """
        while not self.stopped:
            # We can actually see an ~8% increase in FPS by only calling
            # cv2.imshow when a new frame is set with an if statement. Thus,
            # set `self.frame` to None after each call to `cv2.imshow()`.
            if self.frame is not None:
                cv2.imshow(self.win_name, self.frame)
                self.frame = None

            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        cv2.destroyWindow(self.win_name)
        self.stopped = True


video_getter = VideoGetter("http://192.168.8.107:8080/stream/video.mjpeg").start()
video_shower = VideoShower(video_getter.frame).start()


while True:
    if video_getter.stopped or video_shower.stopped:
        video_shower.stop()
        video_getter.stop()
        break

    frame = video_getter.frame    
    video_shower.frame = frame
    