import cv2
import cv2 as cv


class VideoProcess:

    def __init__(self, file):
        self.video_capture = cv.VideoCapture(file)
        while self.video_capture.isOpened():
            ret, frame = self.video_capture.read()
            if ret is True:
                cv.imshow('Frame', frame)
                key = cv2.waitKey(20)
                # some business logic
                if key == ord('q'):
                    self.release()
            else:
                self.release()

    def release(self):
        self.video_capture.release()
        cv.destroyAllWindows()