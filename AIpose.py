import cv2
import numpy as np
import time
from pose import Posedetector
det = Posedetector()


class VideoCamera(object):
    def __init__(self):
        self.path = 0
        self.count = 0
        self.dir = 0
        self.pTime = 0
        self.cap = cv2.VideoCapture(self.path)
        self.font = cv2.FONT_HERSHEY_COMPLEX

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        try:
            success, img = self.cap.read()
            img = cv2.resize(img, (640, 480))
            img = det.findPose(img, False)
            lmList = det.findPosition(img, False)
            cv2.rectangle(img, (0, 0), (125, 168), (107, 106, 41), cv2.FILLED)
            cv2.putText(img, '|workout|', (5, 70), self.font, 0.7, (255, 255, 255), 1)
            if len(lmList) != 0:
                # Right Arm
                angleR = det.findAngle(img, 12, 14, 16)
                # # Left Arm
                angleL = det.findAngle(img, 11, 13, 15)
                per = np.interp(angleR, (210, 310), (0, 100))
                bar = np.interp(angleR, (210, 310), (480, 170))
                # Check for the dumbbell curls
                if per == 0:
                    if self.dir == 0:
                        self.count += 0.5
                        self.dir = 1
                if per == 100:
                    if self.dir == 1:
                        self.count += 0.5
                        self.dir = 0
                # draw Bar
                cv2.rectangle(img, (0, 170), (30, 480), (255, 106, 255), -1)
                cv2.rectangle(img, (0, int(bar)), (30, 170), (107, 106, 41), cv2.FILLED)
                cv2.rectangle(img, (0, 170), (30, 480), (255, 0, 10), 2)
                cv2.putText(img, '{}%'.format(int(per)), (35, 190), self.font, .6, (255, 255, 255), 1)
                cv2.putText(img, str(int(self.count)), (15, 150), self.font, 2, (255, 255, 255), 3)
            cTime = time.time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            cv2.putText(img, 'FPS: '+str(int(fps)), (10, 30), self.font, 0.8, (255, 255, 255), 2)
            ret, jpeg = cv2.imencode('.jpg', img)
            return jpeg.tobytes()
        finally:
            pass
