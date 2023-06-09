# Workshop 2 Group 3
# Group Members:
# 1) Sue Chen Xiang B032010034
# 2. Fatin Najdah binti Najmi Ismail B032010201 
# 3. Nur Afiqah binti Anuar B032010114 
# 4. Ken Prameswari Caesarella B032010461 
# 5. Mohammad Irsyad bin Mohd Shahril B032010242

import tkinter as tk
import tkinter.ttk as ttk
import threading
import re
from PIL import Image, ImageTk
from mysql.connector import connect, Error
from tkinter.messagebox import askokcancel

LARGE_FONT = ("Verdana", 30, "bold")
NORMAL_FONT = ("Verdana", 15, "bold")
SMALL_FONT = ("Verdana", 9)
UNDERLINE_FONT = ("Verdana", 10, "bold", "underline")
UNDERLINE_LARGEFONT = ("Verdana", 15, "bold", "underline")

class CheckOutPage(tk.Toplevel):
    def __init__(self, product_qty, product_price, totalPrice, parent_controller, *args, **kwargs):
        # tk.Tk.__init__(self, *args, **kwargs)
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.wm_title("Check Out")
        self.wm_protocol("WM_DELETE_WINDOW", self.do_nothing)
        self.iconbitmap(default="store_logo.ico")

        self.product_qty = product_qty
        self.product_price = product_price
        self.totalPrice = totalPrice
        self.parent_controller = parent_controller

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.configure(borderwidth=3, relief="solid")

        self.stopEvent = threading.Event()

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

        rightFrame = tk.Frame(self.container, background="#DFDEDE", borderwidth=2, relief="solid")
        rightFrame.pack(side="left", fill="both", expand=True)

        label_payment = tk.Label(rightFrame, text="Payment\n\n\n", font=UNDERLINE_LARGEFONT, width=15)
        label_payment.pack(side="top", fill="both")

        qr = Image.open("qr.png")
        gmbr = ImageTk.PhotoImage(image=qr)
        label = tk.Label(rightFrame, image=gmbr)
        label.pack(side="top", fill="both")
        label.image=gmbr

        detailPanel = tk.Frame(rightFrame, background="#DFDEDE")
        detailPanel.pack(side="top", anchor="w")

        frame1 = tk.Frame(self.container)
        frame1.pack(side="top", anchor="nw", fill="x", expand=True)

        label_summary = tk.Label(frame1, text="Order Summary", font=UNDERLINE_FONT, width=15)
        label_summary.pack(side="top", fill="x")

        frame2 = tk.Frame(frame1)
        frame2.pack(side="top", anchor="nw", fill="x", expand=True)
        frame2.grid_rowconfigure(0, weight=1)
        frame2.grid_columnconfigure(0, weight=3)
        frame2.grid_columnconfigure(1, weight=1)
        frame2.grid_columnconfigure(2, weight=1)
        frame2.grid_columnconfigure(3, weight=1)

        label_name = tk.Label(frame2, text="Items", font=SMALL_FONT, width=25)
        label_name.grid(row=1, column=0, sticky="nw")
        label_price = tk.Label(frame2, text="Price", font=SMALL_FONT, width=5)
        label_price.grid(row=1, column=1, sticky="nsew")
        label_qty = tk.Label(frame2, text="Qty", font=SMALL_FONT, width=4)
        label_qty.grid(row=1, column=2, sticky="nsew")
        label_subtotal = tk.Label(frame2, text="Subtotal", font=SMALL_FONT, width=8)
        label_subtotal.grid(row=1, column=3, sticky="nsew")

        total_item = 0
        for name in self.product_qty:
            if self.product_qty[name] == 0:
                continue
            frame = tk.Frame(frame1, background="#DFDEDE")
            frame.pack(side="top", anchor="w", fill="x", expand=True)
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=3)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid_columnconfigure(2, weight=1)
            frame.grid_columnconfigure(3, weight=1)
            label_name = tk.Label(frame, text=name, font=SMALL_FONT, width=25, anchor="w")
            label_name.grid(row=0, column=0, sticky="nw")
            label_price = tk.Label(frame, text=self.product_price[name], font=SMALL_FONT, width=5)
            label_price.grid(row=0, column=1, sticky="nsew")
            label_qty = tk.Label(frame, text=self.product_qty[name], font=SMALL_FONT, width=4)
            label_qty.grid(row=0, column=2, sticky="nsew")

            qty = self.product_qty[name]
            subtotal = "RM" + str(self.product_price[name] * qty)
            label_subtotal = tk.Label(frame, text=subtotal, font=SMALL_FONT, width=8)
            label_subtotal.grid(row=0, column=3, sticky="nsew")

            total_item += qty

        label_totalitem = tk.Label(frame1, text=f"Total items\t{total_item}", font=NORMAL_FONT, width=8, anchor="w")
        label_totalitem.pack(side="top", fill="x", pady=(100,0))
        label_subtotal2 = tk.Label(frame1, text=f"Subtotal\t\tRM{self.totalPrice}", font=NORMAL_FONT, width=8, anchor="w")
        label_subtotal2.pack(side="top", fill="x")
        label_disc = tk.Label(frame1, text="Disc\t\t0", font=NORMAL_FONT, width=8, anchor="w")
        label_disc.pack(side="top", fill="x")
        label_total = tk.Label(frame1, text=f"Total\t\tRM{self.totalPrice}", font=NORMAL_FONT, width=8, anchor="w")
        label_total.pack(side="top", fill="x")

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

        doneButton = tk.Button(
                        frame1, 
                        text="Done", 
                        background="#55D934", 
                        relief="solid", 
                        width=15, 
                        height=1, 
                        activebackground="green", 
                        font=NORMAL_FONT,
                        command=self.done)
        doneButton.pack(side="bottom", pady=50)

    def show_page(self):
        self.geometry("1280x600")
        self.mainloop()

    def save_sale_record(self):
        transaction_id = 0
        try:
            with connect(host="127.0.0.1", user="root", password="", database="smart_convenience_store") as connection:
                query = """
                    INSERT INTO TRANSACTION (transaction_discount, transaction_total)
                    VALUES (%(discount)s, %(total)s)
                """
                data_tuple = {
                    "discount": 0,
                    "total": self.totalPrice
                }
                with connection.cursor() as cursor:
                    cursor.execute(query, data_tuple)
                    connection.commit()
                
                query = """
                    SELECT transaction_id FROM TRANSACTION ORDER BY transaction_id DESC LIMIT 1
                """
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    for row in result:
                        transaction_id = row[0]

                query = """
                    INSERT INTO SALE 
                    VALUES (%s, %s, %s)
                """
                data_tuple = []
                for product_name in self.product_qty:
                    sale_qty = self.product_qty[product_name]
                    if sale_qty == 0: continue
                    product_id = self.get_product_id_from_db(product_name)
                    data = (transaction_id, product_id, sale_qty)
                    data_tuple.append(data)
                with connection.cursor() as cursor:
                    cursor.executemany(query, data_tuple)
                    connection.commit()

                query = """
                    UPDATE PRODUCT SET product_qty = product_qty - %s WHERE product_id=%s
                """
                data_tuple = []
                for product_name in self.product_qty:
                    sale_qty = self.product_qty[product_name]
                    if sale_qty == 0: continue
                    product_id = self.get_product_id_from_db(product_name)
                    data = (sale_qty, product_id)
                    data_tuple.append(data)
                with connection.cursor() as cursor:
                    cursor.executemany(query, data_tuple)
                    connection.commit()
                
        except Error as e:
            print(e)

    def get_product_id_from_db(self, item):
        product_id = 0
        try:
            with connect(host="127.0.0.1", user="root", password="", database="smart_convenience_store") as connection:
                query = "SELECT product_id FROM PRODUCT WHERE product_item='%s'" % self.camel_case_split(item).strip()
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    for row in result:
                        product_id = row[0]
        except Error as e:
            print(e)

        return product_id

    # function to split camel case
    # string to individual strings
    def camel_case_split(self, str):
        words = re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', str)
        return " ".join(words)

    def cancel(self):
        if askokcancel(title="Cancel Order", message="Are you sure you want to cancel this order?"):
            self.destroy()
            self.parent_controller.deiconify()
    
    def done(self):
        self.save_sale_record()
        self.destroy()
        self.parent_controller.deiconify()
    
    def do_nothing(self):
        pass

if __name__ == "__main__":
    product_qty = {'ApolloChocolateCake': 2, 'ApolloChocolateWaferCream': 2, 'ChipsMoreMini': 1, 'GardeniaCreamRoll': 1, 'MaggiCurry': 1, 'OralBToothBrush': 1}
    product_price = {'ApolloChocolateCake': 1.5, 'ApolloChocolateWaferCream': 0.5, 'ChipsMoreMini': 5, 'GardeniaCreamRoll': 1, 'MaggiCurry': 3, 'OralBToothBrush': 5}
    app = CheckOutPage(product_qty, product_price, 7.5)
    app.show_page()