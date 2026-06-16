import cv2 as cv
import numpy as np
import tkinter as tk
import bcrypt

class Window:
    def __init__(self, size="800x600"):
        self.window = tk.Tk()
        self.window.geometry(size)


class LoginWindow(Window):
    def __init__(self):
        super().__init__()
        self.active = True
        tk.Label(self.window, text="Login", font=("Arial",20)).grid(row=0, column=10)
        tk.Label(self.window, text="Username").grid(row=1, column=9)
        self.user_entry = tk.Entry(self.window, font=('calibre',10,'normal'))
        self.user_entry.grid(row=1, column=10)
        tk.Label(self.window, text="Password").grid(row=2, column=9)
        self.passw_entry = tk.Entry(self.window, font = ('calibre',10,'normal'), show = '*')
        self.passw_entry.grid(row=2, column=10)
        self.login = tk.Button(self.window, text="Login", font=("Arial", 16), command=self.auth(self.user_entry.get(), self.passw_entry.get()))
        self.login.grid(row=3, column=2)
        self.window.mainloop()

    def auth(self, username, password):
        db = DBConnector()
        if db.checkAuth(username, bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())):
            main = MainWindow
            self.active = False
        else:
            pass
            # Show that the password is incorrect



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
    def __init__(self):
        pass
    
    def checkAuth(self, user, pass_hash):
        pass

login = LoginWindow()