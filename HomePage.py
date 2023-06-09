# Workshop 2 Group 3
# Group Members:
# 1) Sue Chen Xiang B032010034
# 2. Fatin Najdah binti Najmi Ismail B032010201 
# 3. Nur Afiqah binti Anuar B032010114 
# 4. Ken Prameswari Caesarella B032010461 
# 5. Mohammad Irsyad bin Mohd Shahril B032010242

import tkinter as tk
import cv2
import threading
from PIL import ImageTk, Image
from tkinter.messagebox import askokcancel
from ProductDetectionPage import ProductDetectionPage
from PeopleCountingPage import PeopleCountingPage
from MonthlySaleReport import MonthlySalePage
from PeopleCountReport import PeopleCountReportPage
from ProductList import ProductListPage

LARGE_FONT = ("Verdana", 30, "bold")
NORMAL_FONT = ("Verdana", 15, "bold")
SMALL_FONT = ("Verdana", 9)

class HomePage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.wm_title("AI COOP: SMART CONVENIENCE STORE")
        self.iconbitmap(default="store_logo.ico")
        self.product_detection_page = None
        self.people_counting_page = None
        self.configure(borderwidth=2, relief="solid")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        topLabel = tk.Label(
                        container, 
                        text="AI COOP: SMART CONVENIENCE STORE", 
                        background="#4E4C67", 
                        foreground="white", 
                        anchor="center", 
                        height=1, 
                        borderwidth=3, 
                        relief="solid", 
                        font=LARGE_FONT)
        topLabel.pack(side="top", fill="x", padx=0.4)

        frame_mainmenu = tk.Frame(container, borderwidth=2, relief="solid", background="#FFD553")
        frame_mainmenu.pack(side="top", fill="both", expand=True)

        for i in range(3):
            frame_mainmenu.grid_rowconfigure(i, weight=1)
            frame_mainmenu.grid_columnconfigure(i, weight=1)

        button_start = tk.Button(
                frame_mainmenu, 
                text="Start System", 
                background="#EDEDED", 
                width=10, 
                height=6, 
                relief="solid", 
                font=NORMAL_FONT, 
                command=self.on_start
            )
        button_start.grid(row=0, column=0, sticky="nsew", padx=30, pady=20, ipadx=0, ipady=0)

        button_product = tk.Button(
                frame_mainmenu, 
                text="View Products", 
                background="#EDEDED", 
                width=10, height=6, 
                relief="solid", 
                font=NORMAL_FONT, 
                command=lambda: ProductListPage().show_page()
            )
        button_product.grid(row=0, column=1, sticky="nsew", padx=(45,45), pady=20)

        button_sale = tk.Button(
                frame_mainmenu, 
                text="View Sales", 
                background="#EDEDED", 
                width=10, 
                height=6, 
                relief="solid", 
                font=NORMAL_FONT, 
                command=lambda: MonthlySalePage().show_page()
            )
        button_sale.grid(row=0, column=2, sticky="nsew", padx=30, pady=20)

        img = cv2.imread("store_logo.png", cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (250,250))
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        logo = tk.Label(frame_mainmenu, image=img, background="#FFD553")
        logo.grid(row=1, column=1, sticky="nsew")
        logo.img = img

        button_people_count = tk.Button(
                frame_mainmenu, 
                text="View People \nCount Statistic", 
                background="#EDEDED", 
                width=10, 
                height=2, 
                relief="solid", 
                font=NORMAL_FONT, 
                command=lambda: PeopleCountReportPage().show_page()
            )
        button_people_count.grid(row=1, column=0, sticky="nsew", padx=30, pady=(35,30))

        button_exit = tk.Button(
                frame_mainmenu, 
                text="Exit System", 
                background="#EDEDED", 
                width=10, 
                height=2, 
                relief="solid", 
                font=NORMAL_FONT, 
                command=self.on_closing
            )
        button_exit.grid(row=1, column=2, sticky="nsew", padx=30, pady=(35,30))

    def show_page(self):
        self.geometry("900x500")
        self.mainloop()

    def on_start(self):
        if self.product_detection_page is not None:
            self.product_detection_page.on_closing()
            self.product_detection_page = None
        if self.people_counting_page is not None:
            self.people_counting_page.on_closing()
            self.people_counting_page = None

        self.product_detection_page = ProductDetectionPage(source=0)
        self.people_counting_page = PeopleCountingPage(source=0)

        thread_pd = threading.Thread(target=self.product_detection_page.show_page, args=(), daemon=True)
        thread_pd.start()

        thread_pc = threading.Thread(target=self.people_counting_page.show_page, args=(), daemon=True)
        thread_pc.start()

    def on_closing(self):
        if askokcancel(title="Exit System", message="Are you sure you want to exit the system?"):
            if self.product_detection_page:
                self.product_detection_page.on_closing()
            if self.people_counting_page:
                self.people_counting_page.on_closing()
            self.destroy()

if __name__ == "__main__":
    app = HomePage()
    app.show_page()