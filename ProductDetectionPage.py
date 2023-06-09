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
from PIL import Image, ImageTk
from tkinter import messagebox
from mysql.connector import connect, Error
from ProductDetectionModule.ProductDetection import ProductDetection
from CheckOutPage import CheckOutPage

LARGE_FONT = ("Verdana", 30, "bold")
NORMAL_FONT = ("Verdana", 15, "bold")
SMALL_FONT = ("Verdana", 9)

class ProductDetectionPage(tk.Toplevel):
    def __init__(self, source=0, *args, **kwargs):
        # tk.Tk.__init__(self, *args, **kwargs)
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.wm_title("Product Detection")
        self.iconbitmap(default="store_logo.ico")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.configure(borderwidth=3, relief="solid")

        self.product_qty = None
        self.product_price = self.get_price_from_db()
        self.stopEvent = threading.Event()
        self.product_detection = ProductDetection()
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
        self.camArea.pack(side="left", fill="y")

        rightFrame = tk.Frame(self.container, background="#DFDEDE", borderwidth=2, relief="solid")
        rightFrame.pack(side="left", fill="both", expand=True)

        detailPanel = tk.Frame(rightFrame, background="#DFDEDE")
        detailPanel.pack(side="top", anchor="w")

        frame = tk.Frame(detailPanel, background="#DFDEDE")
        frame.pack(side="top", anchor="w", fill="x", expand=True)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=3)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=1)
        label_name = tk.Label(frame, text="Items", font=SMALL_FONT, background="#DFDEDE", width=25)
        label_name.grid(row=0, column=0, sticky="nw")
        label_price = tk.Label(frame, text="Price", font=SMALL_FONT, background="#DFDEDE", width=5)
        label_price.grid(row=0, column=1, sticky="nsew")
        label_qty = tk.Label(frame, text="Qty", font=SMALL_FONT, background="#DFDEDE", width=4)
        label_qty.grid(row=0, column=2, sticky="nsew")
        label_subtotal = tk.Label(frame, text="Subtotal", font=SMALL_FONT, background="#DFDEDE", width=8)
        label_subtotal.grid(row=0, column=3, sticky="nsew")

        cancelButton = tk.Button(
                        rightFrame, 
                        text="Cancel", 
                        background="red", 
                        relief="solid", 
                        width=15, 
                        height=1, 
                        activebackground="red", 
                        font=NORMAL_FONT,
                        command=self.cancel)
        cancelButton.pack(side="bottom", pady=5)

        checkOutButton = tk.Button(
                        rightFrame, 
                        text="Check Out", 
                        background="#55D934", 
                        relief="solid", 
                        width=15, 
                        height=1, 
                        activebackground="green", 
                        font=NORMAL_FONT,
                        command=lambda: self.check_out())
        checkOutButton.pack(side="bottom", pady=10)

        calculateButton = tk.Button(
                        rightFrame, 
                        text="Calculate", 
                        background="#FFD553",     
                        relief="solid", 
                        width=15, 
                        height=1, 
                        activebackground="orange", 
                        font=NORMAL_FONT,
                        command=lambda: self.product_count(detailPanel))
        calculateButton.pack(side="bottom", pady=5)

        self.product_detection.start(src=self.source)

        while self.product_detection.wait:
            pass

    def show_page(self):
        thread = threading.Thread(target=self.show_cam, args=(), daemon=True)
        thread.start()
        self.geometry("1280x600")
        self.mainloop()

    def show_cam(self):
        try:
            while not self.stopEvent.is_set():
                frame = self.product_detection.get_frame()
                frame = cv2.resize(frame, (900, 500))

                image = Image.fromarray(frame)
                imagetk = ImageTk.PhotoImage(image=image)

                self.camArea.configure(image=imagetk)
                self.camArea.image = imagetk

                k = cv2.waitKey(20)
        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def product_count(self, parent):
        product_qty = self.product_detection.product_counting()

        if self.product_qty is None:
            self.product_qty = product_qty
            self.product_labels = {}

            for name in product_qty:
                frame = tk.Frame(parent, background="#DFDEDE")
                frame.grid_rowconfigure(0, weight=1)
                frame.grid_columnconfigure(0, weight=3)
                frame.grid_columnconfigure(1, weight=1)
                frame.grid_columnconfigure(2, weight=1)
                frame.grid_columnconfigure(3, weight=1)
                label_name = tk.Label(frame, text="", font=SMALL_FONT, background="#DFDEDE", width=25, anchor="w")
                label_name.grid(row=0, column=0, sticky="nw")
                label_price = tk.Label(frame, text="", font=SMALL_FONT, background="#DFDEDE", width=5)
                label_price.grid(row=0, column=1, sticky="nsew")
                label_qty = tk.Label(frame, text="", font=SMALL_FONT, background="#DFDEDE", width=4)
                label_qty.grid(row=0, column=2, sticky="nsew")
                label_subtotal = tk.Label(frame, text="", font=SMALL_FONT, background="#DFDEDE", width=8)
                label_subtotal.grid(row=0, column=3, sticky="nsew")

                self.product_labels[name] = {
                    "frame": frame, 
                    "name": label_name, 
                    "price": label_price,
                    "qty": label_qty, 
                    "subtotal": label_subtotal
                    }

        for product_name in product_qty:
            if product_qty[product_name] != 0:
                quantity = product_qty[product_name]
                self.product_qty[product_name] = quantity
                price = str(self.product_price[product_name])
                subtotal = "RM" + str(self.product_price[product_name]*quantity)

                self.product_labels[product_name]["name"].configure(text=product_name)
                self.product_labels[product_name]["price"].configure(text=price)
                self.product_labels[product_name]["qty"].configure(text=quantity)
                self.product_labels[product_name]["subtotal"].configure(text=subtotal)
                self.product_labels[product_name]["frame"].pack(side="top", anchor="w", fill="x", expand=True)
    
    def calculate_price(self):
        total_price = 0

        for item in self.product_qty:
            price = self.product_price[item] * self.product_qty[item]
            total_price += price

        return total_price

    def get_price_from_db(self):
        product_price = {}
        try:
            with connect(host="127.0.0.1", user="root", password="", database="smart_convenience_store") as connection:
                query = "SELECT product_item, product_price FROM PRODUCT"
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    for row in result:
                        item = row[0].replace(" ", "")
                        product_price[item] = row[1]
        except Error as e:
            print(e)
        # print(product_price)
        return product_price

    def check_out(self):
        if self.product_qty is None:
            messagebox.showinfo(title="No item selected!!", message="There is currently no product selected!")
            return
        total_price = self.calculate_price()
        self.withdraw()
        check_out_page = CheckOutPage(self.product_qty, self.product_price, total_price, self)
        self.cancel()
        check_out_page.show_page()

    def cancel(self):
        self.product_detection.reset_product_counting()
        self.product_qty = None
        for product_name in self.product_price:
            self.product_labels[product_name]["name"].configure(text="")
            self.product_labels[product_name]["price"].configure(text="")
            self.product_labels[product_name]["qty"].configure(text="")
            self.product_labels[product_name]["subtotal"].configure(text="")
            self.product_labels[product_name]["frame"].pack_forget()
        
    def on_closing(self):
        self.product_detection.end_program()
        self.stopEvent.set()
        self.destroy()

    def do_nothing(self):
        pass

if __name__ == "__main__":
    app = ProductDetectionPage()
    app.show_page()