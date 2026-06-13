import cv2 as cv
import numpy as np
import tkinter as tk
    
class LoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.passw_entry = tk.Entry(self.window, font = ('calibre',10,'normal'), show = '*')
        self.passw_entry.pack()
        self.window.geometry("")
        self.window.mainloop()

class MainWindow:
    def __init__(self):
        self.window = tk.Tk()

class ImageProcessing:
    def __init__(self):
        self.cap = cv.VideoCapture(0)

    def displayCap(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            cv.waitKey(1)
            cv.imshow("Frame", frame)

login = LoginWindow