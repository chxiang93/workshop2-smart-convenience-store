# Workshop 2 Group 3
# Group Members:
# 1) Sue Chen Xiang B032010034
# 2. Fatin Najdah binti Najmi Ismail B032010201 
# 3. Nur Afiqah binti Anuar B032010114 
# 4. Ken Prameswari Caesarella B032010461 
# 5. Mohammad Irsyad bin Mohd Shahril B032010242

import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from tkinter.messagebox import showinfo, askyesno
from mysql.connector import connect, Error

LARGE_FONT = ("Verdana", 30, "bold")
NORMAL_FONT = ("Verdana", 15, "bold")
SMALL_FONT = ("Verdana", 9)

class ProductListPage(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        # tk.Tk.__init__(self, *args, **kwargs)
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.wm_title("Product Information")
        self.iconbitmap(default="store_logo.ico")

        self.product_list = self.get_product_data()

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.configure(borderwidth=3, relief="solid")

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

        result_frame = tk.Frame(self.container, borderwidth=2, relief="solid")
        result_frame.pack(side="top", fill="both", expand=True)

        self.create_table(result_frame)

    def show_page(self):
        self.geometry("1280x600")
        self.mainloop()

    def get_product_data(self):
        product_list = []
        try:
            with connect(host="127.0.0.1", user="root", password="", database="smart_convenience_store") as connection:
                query = "SELECT * FROM PRODUCT"
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    for row in results:
                        print(*row)
                        product = Product(*row)
                        product_list.append(product)
        except Error as e:
            print(e)
        return product_list

    def create_table(self, parent):

        parent.grid_rowconfigure(0, weight=0)
        parent.grid_columnconfigure(1, weight=1)

        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        frame_selection = tk.Frame(parent)
        representation_label = tk.Label(frame_selection, text="Products Information", font=("Verdana", 25, "bold"))
        representation_label.pack()

        frame_selection.grid(row=0, column=0, sticky="nsew")

        columns = ('id', 'name', 'qty', 'price', 'healthiness', 'created', 'updated')
        self.table = ttk.Treeview(parent, columns=columns, show="headings")
        self.table.heading("id", text="Product ID")
        self.table.heading("name", text="Product Item")
        self.table.heading("qty", text="Quantity")
        self.table.heading("price", text="Price(RM)")
        self.table.heading("healthiness", text="Healthiness")
        self.table.heading("created", text="Created")
        self.table.heading("updated", text="Updated")

        self.table.column("id", width=150, anchor="center")
        self.table.column("name", width=200, anchor="center")
        self.table.column("qty", width=150, anchor="center")
        self.table.column("price", width=150, anchor="center")
        self.table.column("healthiness", width=150, anchor="center")
        self.table.column("created", width=150, anchor="center")
        self.table.column("updated", width=150, anchor="center")

        # self.table.bind("<<TreeviewSelect>>", self.item_selected)
        self.table.bind("<Double-1>", self.item_selected)
        self.table.grid(row=1, column=0, sticky="nsew", pady=20, padx=(70,0))

        # add a scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="nwsw")

        for data in self.product_list:
            product_data = (data.id, data.name, data.qty, data.price, data.healthiness, data.created, data.updated)
            self.table.insert("", tk.END, values=product_data)

    def item_selected(self, event):
        for selected_item in self.table.selection():
            item = self.table.item(selected_item)
            record = item["values"]
            self.item_detail_panel(record)

    def item_detail_panel(self, item_data):
        product_label = ("Product ID", "Product Item", "Quantity", "Price(RM)", "Healthiness", "Created", "Updated")
        panel = tk.Toplevel()
        panel.wm_title("Update Product Information")
        nrows = len(item_data)

        panel.grid_columnconfigure(0, weight=1)
        panel.grid_columnconfigure(1, weight=1)
        panel.grid_rowconfigure(nrows, weight=1)

        self.data_entrys_widget = {}
        for row in range(nrows):
            panel.grid_rowconfigure(row, weight=1)

            product_name = tk.Label(panel, width=20, font=SMALL_FONT, text=product_label[row])
            product_name.grid(row=row, column=0, sticky="nsew")

            data_entry = tk.Entry(panel, width=35, font=SMALL_FONT)
            data_entry.grid(row=row, column=1, sticky="nsew")
            data_entry.insert(tk.END, item_data[row])
            data_entry.configure(state="readonly")
            self.data_entrys_widget[product_label[row]] = data_entry

        self.button_cancel = tk.Button(
            panel, 
            text="Cancel", 
            relief="solid", 
            background="red", 
            activebackground="red", 
            width=10, 
            height=2, 
            font=SMALL_FONT, 
            command=lambda: self._cancel_update()
            )

        self.button = tk.Button(
            panel, 
            text="Update", 
            relief="solid", 
            background="#55D934", 
            activebackground="green", 
            width=10,
            height=2, 
            font=SMALL_FONT, 
            command=lambda: self._allow_update()
            )
        self.button.grid(row=nrows, column=1, sticky="nsew", padx=(60,100), pady=15)

        panel.mainloop()

    def _allow_update(self):
        self.button_cancel.grid(row=7, column=0, sticky="nsew", padx=(60,0), pady=15)
        self.button.configure(text="Confirm", command=lambda: self._update_product())
        for entry in self.data_entrys_widget:
            if entry in ("Product ID", "Created", "Updated"):
                continue
            self.data_entrys_widget[entry].configure(state="normal")

    def _update_product(self):
        confirm = askyesno(title="Update Product Information", message="Are you sure you want to update the data of product?")

        if not confirm:
            return

        id = self.data_entrys_widget["Product ID"].get()
        item = self.data_entrys_widget["Product Item"].get()
        qty = self.data_entrys_widget["Quantity"].get()
        price = self.data_entrys_widget["Price(RM)"].get()
        healthiness = self.data_entrys_widget["Healthiness"].get()
        created = self.data_entrys_widget["Created"].get()
        updated = self.data_entrys_widget["Updated"].get()
        print(id, item, qty, price, healthiness, created, updated)
        
        try:
            with connect(host="127.0.0.1", user="root", password="", database="smart_convenience_store") as connection:
                now = datetime.now()
                formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
                query = """
                    UPDATE PRODUCT 
                    SET product_item = %(item)s,
                    product_qty = %(qty)s,
                    product_price = %(price)s,
                    product_healthiness = %(healthiness)s,
                    updated = %(date)s
                    WHERE product_id = %(id)s
                """
                data_dictionary = {
                    "item": item,
                    "qty": int(qty),
                    "price": float(price),
                    "healthiness": healthiness,
                    "date": formatted_date,
                    "id": int(id)
                }
                
                with connection.cursor() as cursor:
                    cursor.execute(query, data_dictionary)
                    connection.commit()
        except Error as e:
            print(e)
        self._cancel_update()

    def _cancel_update(self):
        self.button.configure(text="Update", command=lambda: self._allow_update())
        for entry in self.data_entrys_widget:
            if entry in ("Product ID", "Created", "Updated"):
                continue
            self.data_entrys_widget[entry].configure(state="readonly")
        self.button_cancel.grid_forget()

class Product:
    def __init__(self, id, name, qty, price, healthiness, created, updated): 
        self.id = id
        self.name = name
        self.qty = qty
        self.price = price
        self.healthiness = healthiness
        self.created = created
        self.updated = updated

if __name__ == "__main__":
    app = ProductListPage()
    app.show_page()
