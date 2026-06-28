import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import ttk
import bcrypt
import sqlite3
from datetime import datetime
from os.path import isfile
import os
from PIL import Image, ImageTk
import random
import string

class Window:
    def __init__(self, size="800x600"):
        self.window = tk.Tk()
        self.window.geometry(size)


class LoginWindow(Window):
    def __init__(self):
        super().__init__()
        self.active = True
        tk.Label(self.window, text="Login Window", font=("Arial",20)).place(relx=0.5,rely=0.10,relwidth=0.5,relheight=0.08,anchor="center")
        tk.Label(self.window, text="Username").place(relx=0.5,rely=0.20,anchor="center")
        self.user_entry = tk.Entry(self.window, font=('calibre',10,'normal'))
        self.user_entry.place(relx=0.5,rely=0.25,anchor="center")
        tk.Label(self.window, text="Password").place(relx=0.5,rely=0.30,anchor="center")
        self.passw_entry = tk.Entry(self.window, font = ('calibre',10,'normal'), show = '*')
        self.passw_entry.place(relx=0.5,rely=0.35,anchor="center")
        self.login = tk.Button(self.window, text="Login", font=("Arial", 16), command=self.auth)
        self.login.place(relx=0.5,rely=0.45,anchor="center")
        self.window.mainloop()

    def auth(self):
        db = DBConnector()
        if db.checkAuth(self.user_entry.get(), self.passw_entry.get()):
            self.window.destroy()
            global main
            main = MainWindow()
        else:
            print("Incorrect login")



class MainWindow(Window):
    def __init__(self):
        super().__init__("1200x1600")
        self.camstream = ImageProcessing()
        self.imageLabel = tk.Label(self.window)
        self.imageLabel.pack()
        self.delbutton = tk.Button(self.window, text="Delete clip", command=self.deleteClip)
        self.delbutton.pack()
        self.table = ttk.Treeview(self.window)
        self.table['columns'] = ('EventID', 'Timestamp', 'CamID', 'Vid_Name')
        self.table.column('#0', width=0, stretch=tk.NO)
        self.table.column('EventID', anchor=tk.W, width=200)
        self.table.column('Timestamp', anchor=tk.W, width=200)
        self.table.column('CamID', anchor=tk.W, width=100)
        self.table.column('Vid_Name', anchor=tk.W, width=200)

        # Create the headings
        self.table.heading('#0', text='', anchor=tk.W)
        self.table.heading('EventID', text='EventID', anchor=tk.W)
        self.table.heading('Timestamp', text='Timestamp', anchor=tk.W)
        self.table.heading('CamID', text='CamID', anchor=tk.W)
        self.table.heading('Vid_Name', text='Vid_Name', anchor=tk.W)
        self.table.pack()
        self.refreshTable()

        self.window.after(0,self.camLoop)

        self.window.mainloop()

    def camLoop(self):
        frame, tkFrame = self.camstream.displayCap()
        self.imageLabel.photo_image = tkFrame
        self.imageLabel.configure(image=tkFrame)
        if self.camstream.refresh:
            self.refreshTable()
        self.window.after(50, self.camLoop)
    
    def deleteClip(self):
        db = DBConnector()
        curItem = self.table.focus()
        db.removeEvent(self.table.item(curItem)['values'][0])
        os.remove(self.table.item(curItem)['values'][3])
        self.refreshTable()

    def refreshTable(self):
        self.table.delete(*self.table.get_children())
        db = DBConnector()
        for record in db.selectAllEvents():
            self.table.insert(
                "",
                tk.END,
                values=(
                    record[1],
                    record[2],
                    record[3],
                    record[4],
                ),
            )

    def openSettings(self):
        pass

class adminWindow(Window):
    def __init__(self):
        super().__init__( )


class ImageProcessing:
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        
        self.recording = False
        self.refresh = False
        self.filename = None


        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))
        self.fourcc = cv.VideoWriter_fourcc(*'XVID') 

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
        mask = cv.medianBlur(mask, 5)
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel, iterations=1)

        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        cv.drawContours(frame, contours, -1, (0, 255, 0), 3)

        self.final_img = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)

        return self.final_img
    
    def checkMovement(self, grey_arr):
        if np.count_nonzero(grey_arr) > 100000:
            self.record(True)
        else:
            self.record()


    def record(self,movement = False):
        self.refresh = False

        if movement and not self.recording:
            self.recording = True
            self.startTime = datetime.now()
            self.filename = "output1.avi"
            while isfile(self.filename):
                self.filename = self.filename[:6] + str(int(self.filename[6]) + 1) + ".avi"
            self.out = cv.VideoWriter(self.filename, self.fourcc, 16, (self.frame_width, self.frame_height))
            print("Start recording")
            
        elif (datetime.now() - self.startTime).total_seconds() < 10 and self.recording:
            self.out.write(cv.cvtColor(self.final_img, cv.COLOR_RGBA2BGR))
            print("Recording")

        else:
            if self.recording:
                print("End recording")
                db = DBConnector()
                db.addEvent("".join(random.choices(string.ascii_letters + string.digits,k=8)), self.startTime, 0, self.filename)
                self.recording = False
                self.refresh = True
                self.out.release()
            else:
                print("Not recording")


    


class DBConnector:
    def __init__(self):
        self.con=sqlite3.connect("MotionRecordingApp.db")
        self.cursor=self.con.cursor()
    
    def createTables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                        username varchar PRIMARY KEY,
                        password varchar NOT NULL
                        );""")

        self.cursor.execute("INSERT INTO users(username,password) VALUES (?,?)",("admin", bcrypt.hashpw(b"admin", bcrypt.gensalt())))

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS events(
                        num integer PRIMARY KEY AUTOINCREMENT,
                        event_id varchar NOT NULL,
                        time timestamp NOT NULL,
                        cam_id integer NOT NULL,
                        vid_name varchar NOT NULL
                        );""")
        
        self.con.commit()
    
    def addEvent(self, event_id, timestamp, cam_id, vid_name):
        self.cursor.execute("INSERT INTO events(event_id, time, cam_id, vid_name) VALUES (?,?,?,?)", (event_id, timestamp.strftime("%Y-%m-%d %H:%M:%S"), cam_id, vid_name))

        self.con.commit()

    def removeEvent(self, event_id):
        self.cursor.execute(f"DELETE FROM events WHERE event_id = \'{event_id}\'")
        
        self.con.commit()

    def selectAllEvents(self):
        query = "SELECT * FROM events"
        output = self.cursor.execute(query)
        return output


    def checkAuth(self, user, password):
        query = f"SELECT password FROM users WHERE username = \'{user}\'"
        output = self.cursor.execute(query)
        for record in output:
            for item in record:
                pass_hash = item
        
        password = password.encode('utf-8')

        return (bcrypt.checkpw(password,pass_hash))

main = MainWindow()