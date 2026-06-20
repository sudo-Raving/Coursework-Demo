import cv2 as cv
import numpy as np
import tkinter as tk
import bcrypt
import sqlite3
from os.path import isfile
from PIL import Image, ImageTk

class Window:
    def __init__(self, size="800x600"):
        self.window = tk.Tk()
        self.window.geometry(size)


class LoginWindow(Window):
    def __init__(self):
        super().__init__()
        self.active = True
        tk.Label(self.window, text="Login", font=("Arial",20)).place(relx=0.5,rely=0.10,relwidth=0.5,relheight=0.08,anchor="center")
        tk.Label(self.window, text="Username").place(relx=0.5,rely=0.20,anchor="center")
        self.user_entry = tk.Entry(self.window, font=('calibre',10,'normal'))
        self.user_entry.place(relx=0.5,rely=0.25,anchor="center")
        tk.Label(self.window, text="Password").place(relx=0.5,rely=0.30,anchor="center")
        self.passw_entry = tk.Entry(self.window, font = ('calibre',10,'normal'), show = '*')
        self.passw_entry.place(relx=0.5,rely=0.35,anchor="center")
        self.login = tk.Button(self.window, text="Login", font=("Arial", 16), command=self.auth(self.user_entry.get(), self.passw_entry.get()))
        self.login.place(relx=0.5,rely=0.45,anchor="center")
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
        super().__init__("1200x1600")
        self.camstream = ImageProcessing()
        self.imageLabel = tk.Label(self.window)
        self.imageLabel.pack()
        self.camLoop()
        self.cambutton = tk.Button(self.window, text="Camera on")
        self.cambutton.pack()
        self.window.mainloop()

    def camLoop(self):
        frame, tkFrame = self.camstream.displayCap()
        self.imageLabel.photo_image = tkFrame
        self.imageLabel.configure(image=tkFrame)
        self.window.after(50, self.camLoop)

    def openSettings(self):
        pass

class adminWindow(Window):
    def __init__(self):
        super().__init__( )


class ImageProcessing:
    def __init__(self):
        self.cap = cv.VideoCapture(0)

    def displayCap(self):
        ret, frame_last = self.cap.read()

        proc_image = self.processImage(frame_last)

        workingImage = Image.fromarray(proc_image)
        workingImage = workingImage.resize((640,480))
        tkFrame = ImageTk.PhotoImage(image=workingImage)

        return frame_last, tkFrame
    
    def processImage(self, frame_last):
        kernel = np.ones((3,3), dtype=np.uint8)

        grey_last = cv.cvtColor(frame_last, cv.COLOR_BGR2GRAY)
        ret, frame = self.cap.read()
        
        grey = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        grey_diff = cv.subtract(grey, grey_last)
        grey_diff = cv.medianBlur(grey_diff, 3)

        self.checkMovement(grey_diff)

        mask = cv.adaptiveThreshold(grey_diff, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV, 11, 3)
        mask = cv.medianBlur(mask, 3)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel, iterations=1)

        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(frame, contours, -1, (0, 255, 0), 3)

        final_img = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)

        return final_img
    
    def checkMovement(self, grey_arr):
        if np.count_nonzero(grey_arr) > 500:
            print("Movement detected")
        else:
            print("No movement")
    


class DBConnector:
    def __init__(self, create=False):
        self.con=sqlite3.connect("MotionRecordingApp.db")
        self.cursor=self.con.cursor
        if create:
            self.createTables()
    
    def createTables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                        username varchar PRIMARY KEY,
                        password varchar NOT NULL,
                        );""")

    def checkAuth(self, user, pass_hash):
        pass

main = MainWindow()