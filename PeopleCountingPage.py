# Workshop 2 Group 3
# Group Members:
# 1) Sue Chen Xiang B032010034
# 2. Fatin Najdah binti Najmi Ismail B032010201 
# 3. Nur Afiqah binti Anuar B032010114 
# 4. Ken Prameswari Caesarella B032010461 
# 5. Mohammad Irsyad bin Mohd Shahril B032010242

import tkinter as tk
import tkinter.ttk as ttk
import cv2
import threading
from datetime import datetime
from PIL import Image, ImageTk
from mysql.connector import connect, Error
from tkinter.messagebox import showwarning
from PeopleCountingModule.PeopleCounting import PeopleCounting

LARGE_FONT = ("Verdana", 30, "bold")
NORMAL_FONT = ("Verdana", 15, "bold")
SMALL_FONT = ("Verdana", 9)

class PeopleCountingPage(tk.Toplevel):
    def __init__(self, source=0, *args, **kwargs):
        # tk.Tk.__init__(self, *args, **kwargs)
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.wm_title("People Detection")
        self.iconbitmap(default="store_logo.ico")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.configure(borderwidth=3, relief="solid")

        self.stopEvent = threading.Event()
        self.people_counter = PeopleCounting()
        self.source = source

        topLabel = tk.Label(
                        self.container, 
                        text="AI COOP: SMART CONVENIENCE STORE", 
                        background="#4E4C67", 
                        foreground="white", 
                        anchor="center", 
                        height=1, 
                        borderwidth=3, 
                        relief="solid", 
                        font=LARGE_FONT)
        topLabel.pack(side="top", fill="x", padx=0.4)

        self.camArea = tk.Label(
                        self.container, 
                        text="Cam", 
                        width=950, 
                        background="white", 
                        foreground="white", 
                        font=LARGE_FONT,
                        borderwidth=2,
                        relief="solid")
        self.camArea.pack(side="top", fill="both", expand=True)

        self.peopleCount_label = tk.Label(self.container, text="People Count: 0", font=NORMAL_FONT)
        self.peopleCount_label.pack(side="left", padx=30)

        self.peopleInside_label = tk.Label(self.container, text="Total People Inside: 0", font=NORMAL_FONT)
        self.peopleInside_label.pack(side="left", padx=100)

        self.close_button = tk.Button(
                        self.container, 
                        text="Close People Counter", 
                        background="red", 
                        relief="solid", 
                        width=20, 
                        height=1, 
                        activebackground="red", 
                        font=NORMAL_FONT,
                        command=self.on_closing)
        self.close_button.pack(side="right", anchor="e", padx=20, pady=5)

        self.people_counter.start(src=self.source)

        while self.people_counter.wait:
            pass

    def show_page(self):
        thread = threading.Thread(target=self.show_cam, args=(), daemon=True)
        thread.start()
        self.geometry("1280x600")
        self.mainloop()

    def show_cam(self):
        try:
            while not self.stopEvent.is_set():
                frame = self.people_counter.getFrames()
                frame = cv2.resize(frame, (1000, 450))

                image = Image.fromarray(frame)
                imagetk = ImageTk.PhotoImage(image=image)

                self.camArea.configure(image=imagetk)
                self.camArea.image = imagetk

                people_count = self.people_counter.peopleCountDay
                people_inside = self.people_counter.peopleInside

                self.peopleCount_label.configure(text=f"People Count: {people_count}")
                self.peopleInside_label.configure(text=f"Total People Inside: {people_inside}")

                k = cv2.waitKey(20)
        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def save_data_to_db(self):
        try:
            with connect(host="127.0.0.1", user="root", password="", database="smart_convenience_store") as connection:
                now = datetime.now()
                formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
                query = """
                    INSERT INTO people_counting VALUES (%s, %s)
                """
                data_tuple = (formatted_date, self.people_counter.peopleCountDay)
                
                with connection.cursor() as cursor:
                    cursor.execute(query, data_tuple)
                    connection.commit()
        except Error as e:
            print(e)

    def checkPeopleInside(self):
        isPeopleInside = False
        if self.people_counter.peopleInside > 0:
            isPeopleInside = True
            showwarning(title="People Inside", message="There are still people inside the store")
        return isPeopleInside

    def on_closing(self):
        if self.checkPeopleInside():
            return
        self.stopEvent.set()
        self.save_data_to_db()
        self.destroy()

if __name__ == "__main__":
    app = PeopleCountingPage()
    app.show_page()