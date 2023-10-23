import cv2
import imutils
import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

gun_cascade = cv2.CascadeClassifier('cascade.xml')

class VideoPlayer:
    def __init__(self, window):
        self.window = window
        self.window.title("Weapon detector")
        self.window.geometry('350x600')
        self.window.configure(bg="black")

        self.canvas = tk.Canvas(window, width=500, height=500)
        self.canvas.pack()
        self.canvas.configure(bg="black")

        self.button = tk.Button(window, text="Open video", command=self.open_video, width = 10, height= 2, bg='white', font='Georgia 13')
        self.button.pack(side="bottom")

        self.video = None
        self.video_stream = None
        self.first_frame = None
        self.gun_exist = False

    def open_video(self):
        video_path = tk.filedialog.askopenfilename(filetypes=[("Video files", "*.mp4")])
        if video_path:
            self.video_stream = cv2.VideoCapture(video_path)
            self.play_video()

    def play_video(self):
        ret, frame = self.video_stream.read()

        if ret:
            frame = imutils.resize(frame, width=350)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize=(100, 100))

            if len(gun) > 2:
                self.gun_exist = True
                message = "ОБНАРУЖЕНА УГРОЗА"
                color = 'red'
                label = tk.Label(self.window, text=message, height=2, font='Georgia 20 bold', bg="white", fg=color)
                label.pack()

            for (x, y, w, h) in gun:
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            self.show_frame(frame)
            self.window.after(1, self.play_video)
        else:
            self.finish_video()
            self.gun_exist = False



    def show_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image)

        if self.video is None:
            self.video = self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        else:
            self.canvas.itemconfig(self.video, image=photo)

        self.canvas.image = photo

    def finish_video(self):
        self.video_stream.release()

        if self.gun_exist:
            print("guns detected")
        else:
            message = "Угроз не обнаружено"
            color = 'green'
            label = tk.Label(self.window, text=message, height=2, font='Georgia 20 bold', bg="white", fg=color)
            label.pack()
            print("guns NOT detected")



window = tk.Tk()
window.title("Weapon Detector App")
window.geometry('350x600')
window.configure(bg="black")
player = VideoPlayer(window)
window.mainloop()