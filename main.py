import cv2 as cv
import numpy as np

class GUI:
    pass

class MainWindow:
    pass

class ImageProcessing:
    def __init__(self):
        self.cap = cv.VideoCapture(0)

    def displayCap(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            
            cv.imshow("Frame", frame)


img_proc = ImageProcessing()
img_proc.displayCap()
    