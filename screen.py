# adapted from https://nickhuber.ca/blog/python-opencv-camera-websockets
import pyautogui as pg
import numpy as np
import threading
import time
import cv2


class Screen:

    def __init__(self, camIndex):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.thread = None
        self.current_frame = None
        self.is_running: bool = False

    def screenshot(self):
        pim = pg.screenshot().convert('RGB')
        nimg = np.array(pim)
        return cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)

    def start(self):
        if self.thread is None:
            self.thread = threading.Thread(target=self._capture)
            self.thread.start()

    def get_frame(self):
        return self.current_frame

    def get_faces(self):
        return self.faces

    def stop(self):
        self.is_running = False
        self.thread.join()
        self.thread = None
        self.current_frame = None

    def _capture(self):
        self.is_running = True
        while self.is_running:
            time.sleep(0.04)
            frame = self.screenshot()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            abs_faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            rel_faces = []
            index = 0

            for (x, y, w, h) in abs_faces:
                index += 1
                face = {}
                face['id'] = index
                face['x'] = x / self.frame_width
                face['y'] = y / self.frame_height
                face['w'] = w / self.frame_width
                face['h'] = h / self.frame_height

                rel_faces.append(face)

            self.current_frame = frame
            self.faces = rel_faces

        print("Camera thread stopped")
        self.thread = None
        self.is_running = False
        self.current_frame = None
