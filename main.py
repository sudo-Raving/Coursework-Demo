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
        tk.Label(self.window, text="Login", font=("Arial",20)).place(relx=0.5,rely=0.1,relwidth=0.5,relheight=0.08,anchor="center")
        tk.Label(self.window, text="Username").place(relx=0.5,rely=0.15,anchor="center")
        self.user_entry = tk.Entry(self.window, font=('calibre',10,'normal'))
        self.user_entry.place(relx=0.5,rely=0.2,anchor="center")
        tk.Label(self.window, text="Password").grid(row=2, column=9)
        self.passw_entry = tk.Entry(self.window, font = ('calibre',10,'normal'), show = '*')
        self.passw_entry.place(relx=0.5,rely=0.4,anchor="center")
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
        super().__init__()
        self.camstream = ImageProcessing()
        self.cambutton = tk.Button(self.window, text="Camera on", command=self.camLoop)
        self.cambutton.pack()
        self.window.mainloop()

    def camLoop(self):
        frame = self.camstream.displayCap()
        cv.imshow("Frame", frame)
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
        ret, frame = self.cap.read()
        return frame
    


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

login = LoginWindow()