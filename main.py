import cv2
import tkinter as tk
import imutils
import numpy as np
from tkinter import filedialog
from PIL import Image, ImageTk
import time

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

        self.button = tk.Button(window, text="Open video", command=self.open_video, width=10, height=2, bg='white', font='Georgia 13')
        self.button.pack(side="bottom")

        self.video = None
        self.video_stream = None
        self.gun_exist = False
        self.frame_count = 0
        self.last_save_time = time.time()

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
            guns = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize=(100, 100))

            for (x, y, w, h) in guns:
                similarity_prob = self.compute_similarity_probability(frame, (x, y, w, h))

                #cv2.putText(frame, f"Probability: {similarity_prob:.2%}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                if similarity_prob > 0.75:
                    self.gun_exist = True
                    message = "ОБНАРУЖЕНА УГРОЗА"
                    color = 'red'
                    label = tk.Label(self.window, text=message, height=2, font='Georgia 20 bold', bg="white", fg=color)
                    label.pack()

                #frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            self.show_frame(frame)

            current_time = time.time()
            elapsed_time = current_time - self.last_save_time
            if elapsed_time >= 10:  # Сохраняем каждые 5 секунд
                self.last_save_time = current_time
                self.save_frame(frame)

            self.window.after(1, self.play_video)
        else:
            self.finish_video()
            self.gun_exist = False

    def compute_similarity_probability(self, frame, roi):
        frame_area = frame.shape[0] * frame.shape[1]
        x, y, w, h = roi
        object_area = w * h
        probability = (object_area / frame_area) * 10
        if probability >= 1:
            probability = 0.86
        elif probability >= 0.86:
            probability = 0.75
        elif probability >= 0.70:
            probability = 0.55

        return probability

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

    def save_frame(self, frame):
        self.frame_count += 1
        cv2.imwrite(f"C:/Users/EasyNote/PycharmProjects/Project_TII/venv/saved_frame7/frame_{self.frame_count}.jpg", frame)

        print(f"Frame {self.frame_count} saved")

window = tk.Tk()
window.title("Weapon Detector App")
window.geometry('350x600')
window.configure(bg="black")
player = VideoPlayer(window)
window.mainloop()
