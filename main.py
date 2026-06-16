import cv2 as cv
import numpy as np
import tkinter as tk

class Window:
    def __init__(self, size="800x600"):
        self.window = tk.Tk()
        self.window.geometry(size)


class LoginWindow(Window):
    def __init__(self):
        super().__init__()
        self.active = True
        tk.Label(self.window, text="Login", font=("Arial",20)).pack()
        tk.Label(self.window, text="Username").pack()
        self.user_entry = tk.Entry(self.window, font=('calibre',10,'normal'))
        self.user_entry.pack()
        tk.Label(self.window, text="Password").pack()
        self.passw_entry = tk.Entry(self.window, font = ('calibre',10,'normal'), show = '*')
        self.passw_entry.pack()
        self.login = tk.Button(self.window, text="Login", font=("Arial", 16), command=self.auth(self.user_entry.get(), self.passw_entry.get()))
        self.login.pack()
        self.window.mainloop()

    def auth(self, username, password):
        db = DBConnector()



class MainWindow(Window):
    def __init__(self):
        super().__init__()

class adminWindow(Window):
    def __init__(self):
        super().__init__( )


class ImageProcessing:
    def __init__(self):
        self.cap = cv.VideoCapture(0)

    def displayCap(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            cv.waitKey(1)
            cv.imshow("Frame", frame)

class DBConnector:
    pass

login = LoginWindow()