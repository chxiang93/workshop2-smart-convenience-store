# Workshop 2 Group 3
# Group Members:
# 1) Sue Chen Xiang B032010034
# 2. Fatin Najdah binti Najmi Ismail B032010201 
# 3. Nur Afiqah binti Anuar B032010114 
# 4. Ken Prameswari Caesarella B032010461 
# 5. Mohammad Irsyad bin Mohd Shahril B032010242

import tkinter as tk
import tkinter.ttk as ttk
import matplotlib
import numpy as np
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mysql.connector import connect, Error

LARGE_FONT = ("Verdana", 30, "bold")
NORMAL_FONT = ("Verdana", 15, "bold")
SMALL_FONT = ("Verdana", 9)
CLASSES = ['ApolloChocolateCake', 'ApolloChocolateWaferCream', 'ChipsMoreMini', 'GardeniaCreamRoll', 'MaggiCurry', 'OralBToothBrush']

class MonthlySalePage(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        # tk.Tk.__init__(self, *args, **kwargs)
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.wm_title("Sale Report")
        self.iconbitmap(default="store_logo.ico")

        self.transaction_list = self.get_transaction_data()
        self.is_canvas_created = False

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

        self.create_report(result_frame)

    def show_page(self):
        self.geometry("1280x600")
        self.mainloop()

    def get_transaction_data(self):
        transaction_list = []
        try:
            with connect(host="127.0.0.1", user="root", password="", database="smart_convenience_store") as connection:
                query = """
                    SELECT * FROM TRANSACTION
                """
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    for row in results:
                        print(*row)
                        transaction = Transaction(row[0], row[1], row[2], row[3])
                        transaction_list.append(transaction)
        except Error as e:
            print(e)
        return transaction_list
    
    def get_sale_based_on_transaction_id(self, transaction_id):
        sale_list = []
        try:
            with connect(host="127.0.0.1", user="root", password="", database="smart_convenience_store") as connection:
                #TODO: sum up
                query = """
                    SELECT transaction_id, product_id, PRODUCT.product_item, PRODUCT.product_price, SALE.sale_quantity
                    FROM TRANSACTION JOIN SALE 
                    USING (transaction_id) 
                    JOIN PRODUCT 
                    Using (product_id) 
                    WHERE transaction_id = %(transaction_id)s
                """
                data_tuple = {"transaction_id": transaction_id}
                with connection.cursor() as cursor:
                    cursor.execute(query, data_tuple)
                    results = cursor.fetchall()
                    for row in results:
                        sale_data = Transaction_Sale(row[1], row[2], row[3], row[4])
                        sale_list.append(sale_data)
        except Error as e:
            print(e)
        print(sale_list)
        return sale_list

    def get_transaction_data_based_on_date(self):
        transaction_list = {"year": [], "month": [], "total": []}
        try:
            with connect(host="127.0.0.1", user="root", password="", database="smart_convenience_store") as connection:
                #TODO: sum up
                query = """
                    SELECT YEAR(created) as year, MONTH(created) as month, SUM(transaction_total) as total 
                    FROM TRANSACTION 
                    GROUP BY year, month 
                    ORDER BY year, month
                """
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    for row in results:
                        transaction_list["year"].append(row[0])
                        transaction_list["month"].append(row[1])
                        transaction_list["total"].append(row[2])
        except Error as e:
            print(e)
        print(transaction_list)
        return transaction_list
    
    def get_most_purchased_product(self):
        product_list = {"year": [], "month": [], "product": [], "qty": []} 
        try:
            with connect(host="127.0.0.1", user="root", password="", database="smart_convenience_store") as connection:
                #TODO: sum up
                query = """
                    SELECT YEAR(transaction.created) as year, MONTH(transaction.created) as month, product_item, SUM(sale_quantity) as qty 
                    FROM TRANSACTION JOIN SALE 
                    USING (transaction_id) 
                    JOIN PRODUCT 
                    Using (product_id) 
                    GROUP BY year, month, product_id 
                    ORDER BY year, month, qty DESC 
                """
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    for row in results:
                        product_list["year"].append(row[0])
                        product_list["month"].append(row[1])
                        product_list["product"].append(row[2])
                        product_list["qty"].append(row[3])
        except Error as e:
            print(e)
        print(product_list)
        return product_list

    def create_report(self, parent):
        frame_selection = tk.Frame(parent)
        representation_label = tk.Label(frame_selection, text="Sales Information", font=("Verdana", 25, "bold"))
        representation_label.pack()

        option_label = tk.Label(frame_selection, text="Choose representation:", font=NORMAL_FONT)
        option_label.pack(side="top")
        
        option_cb = ttk.Combobox(frame_selection, values=("Table", "Graph"), state="readonly")
        option_cb.set("Table")
        option_cb.pack(side="top")
        option_cb.bind("<<ComboboxSelected>>", self._selected_representation)

        frame_selection.pack(side="top", fill="x")

        self.frame_table = tk.Frame(parent)
        self.frame_table.pack(side="top", fill="both", expand=True)

        self.frame_graph = tk.Frame(parent)

        self._create_table(self.frame_table)

    def _selected_representation(self, event):
        option = event.widget.get()
        if option == "Table":
            self._create_table(self.frame_table)
            pass
        elif option == "Graph":
            self._create_graph(self.frame_graph)
            self.is_canvas_created = True

    def _create_table(self, parent):
        self.frame_graph.pack_forget()
        parent.pack(side="top", fill="both", expand=True)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

        columns = ('id', 'discount', 'total', 'created')
        self.table = ttk.Treeview(parent, columns=columns, show="headings")
        self.table.heading("id", text="Transaction ID")
        self.table.heading("discount", text="Discount")
        self.table.heading("total", text="Total(RM)")
        self.table.heading("created", text="Created")

        self.table.column("id", width=100, anchor="center")
        self.table.column("discount", width=100, anchor="center")
        self.table.column("total", width=100, anchor="center")
        self.table.column("created", width=100, anchor="center")

        # self.table.bind("<<TreeviewSelect>>", self.item_selected)
        self.table.bind("<Double-1>", self.item_selected)
        self.table.grid(row=0, column=0, sticky="nsew", pady=20, padx=(250,0))

        # add a scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="nwsw")

        for data in self.transaction_list:
            transaction_data = (data.id, data.discount, data.total, data.created_date)
            self.table.insert("", tk.END, values=transaction_data)

    def _create_graph(self, parent):
        self.frame_table.pack_forget()
        parent.pack(side="top", fill="both", expand=True)

        month_map = {1: "Jan", 2: "Feb", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
                     8: "August", 9: "Sept", 10: "Oct", 11: "Nov", 12: "Dec"}
        sale_date_month = []
        transaction_data = self.get_transaction_data_based_on_date()
        most_purchased_product = self.get_most_purchased_product()

        for year, month in zip(transaction_data["year"], transaction_data["month"]):
            date_month = month_map[month]
            date = str(year) + " " + date_month
            sale_date_month.append(date)

        most_purchased_product_dict = {label: [0 for i in range(len(sale_date_month))] for label in CLASSES}
        print(most_purchased_product_dict)
        i = 0
        for year, month in zip(transaction_data["year"], transaction_data["month"]):
            print(year, month)
            for year_product, month_product, product, qty in zip(most_purchased_product["year"], most_purchased_product["month"], most_purchased_product["product"], most_purchased_product["qty"]):
                print(year_product, month_product)
                if year_product == year and month_product == month:
                    product = product.replace(" ", "")
                    print(product)
                    most_purchased_product_dict[product][i] = int(qty)
            i += 1
        print(most_purchased_product_dict)
        x = np.arange(len(sale_date_month))  # the label locations
        width = 0.03  # the width of the bars

        f = Figure(figsize=(3,3), dpi=100)
        a = f.add_subplot(111)

        # a.plot(["Sept", "Oct", "Nov", "Dec"], [10, 13, 15, 20])
        a.plot(sale_date_month, transaction_data["total"], label="Amount(RM)", linestyle="solid")

        a.bar(x - width*2, most_purchased_product_dict["ApolloChocolateCake"], width, label="Apollo Chocolate Cake")
        a.bar(x - width, most_purchased_product_dict["ApolloChocolateWaferCream"], width, label="Apollo Chocolate Wafer Cream")
        a.bar(x, most_purchased_product_dict["ChipsMoreMini"], width, label="Chips More Mini")
        a.bar(x + width, most_purchased_product_dict["GardeniaCreamRoll"], width, label="Gardenia Cream Roll")
        a.bar(x + width*2, most_purchased_product_dict["MaggiCurry"], width, label="Maggi Curry")
        a.bar(x + width*3, most_purchased_product_dict["OralBToothBrush"], width, label="Oral B Tooth Brush")

        a.legend()

        if not self.is_canvas_created:
            canvas = FigureCanvasTkAgg(f, parent)
            canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

            toolbar = NavigationToolbar2Tk(canvas, parent)
            toolbar.update()
            canvas._tkcanvas.pack(side="top", fill="both", expand=True)

    def item_selected(self, event):
        for selected_item in self.table.selection():
            item = self.table.item(selected_item)
            record = item["values"]
            self.item_detail_panel(record[0])

    def item_detail_panel(self, transaction_id):
        panel = tk.Toplevel(background="black")
        panel.wm_title("Update Product Information")
        panel.resizable(True, False)
        sale_data = self.get_sale_based_on_transaction_id(transaction_id)
        nrows = len(sale_data)

        panel.grid_columnconfigure(0, weight=1)

        transaction_id_label = tk.Label(panel, text=f"Transaction ID : {transaction_id}", font=NORMAL_FONT, anchor="w", background="#DFDEDE")
        transaction_id_label.grid(row=0, column=0, sticky="nsew", pady=(0, 3))

        frame = tk.Frame(panel, background="#DFDEDE")
        frame.grid(row=1, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_columnconfigure(3, weight=1)
        label_id = tk.Label(frame, text="ProductID", font=("Verdana", 9, "bold"), background="#DFDEDE", width=20, anchor="w")
        label_id.grid(row=0, column=0, sticky="nw")
        label_item = tk.Label(frame, text="Item", font=("Verdana", 9, "bold"), background="#DFDEDE", width=30, anchor="w")
        label_item.grid(row=0, column=1, sticky="nw")
        label_price = tk.Label(frame, text="Price", font=("Verdana", 9, "bold"), background="#DFDEDE", width=10, anchor="w")
        label_price.grid(row=0, column=2, sticky="nw")
        label_qty = tk.Label(frame, text="Quantity", font=("Verdana", 9, "bold"), background="#DFDEDE", width=10, anchor="w")
        label_qty.grid(row=0, column=3, sticky="nw")

        for i, sale in enumerate(sale_data):
            panel.grid_rowconfigure(i, weight=1)
            # panel.grid_columnconfigure(i, weight=1)
            frame = tk.Frame(panel, background="#DFDEDE")
            # frame.pack(side="top", anchor="w", fill="x", expand=True)
            frame.grid(row=i+2, column=0, sticky="nsew")
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid_columnconfigure(2, weight=1)
            frame.grid_columnconfigure(3, weight=1)
            label_id = tk.Label(frame, text=sale.product_id, font=SMALL_FONT, background="#DFDEDE", width=20, anchor="w")
            label_id.grid(row=0, column=0, sticky="nsew")
            label_item = tk.Label(frame, text=sale.product_item, font=SMALL_FONT, background="#DFDEDE", width=30, anchor="w")
            label_item.grid(row=0, column=1, sticky="nsew")
            label_price = tk.Label(frame, text=f"RM{sale.product_price}", font=SMALL_FONT, background="#DFDEDE", width=10, anchor="w")
            label_price.grid(row=0, column=2, sticky="nsew")
            label_qty = tk.Label(frame, text=sale.qty, font=SMALL_FONT, background="#DFDEDE", width=10, anchor="w")
            label_qty.grid(row=0, column=3, sticky="nsew")

        total_paid = 0
        for transaction in self.transaction_list:
            if transaction.id == transaction_id:
                total_paid = transaction.total

        frame = tk.Frame(panel, background="#DFDEDE")
        frame.grid(row=nrows+2, column=0, sticky="nsew", pady=(3, 0))
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        label_paid = tk.Label(frame, text=f"Total Paid:   RM{total_paid}", font=NORMAL_FONT, background="#DFDEDE", anchor="w")
        label_paid.grid(row=0, column=0, sticky="nsew", pady=5)

        panel.mainloop()

class Transaction:
    def __init__(self, id, discount, total, created_date):
        self.id = id
        self.discount = discount
        self.total = total
        self.created_date = created_date

class Transaction_Sale:
    def __init__(self, product_id, product_item, product_price, qty):
        self.product_id = product_id
        self.product_item = product_item
        self.product_price = product_price
        self.qty = qty

if __name__ == "__main__":
    m = MonthlySalePage()
    m.show_page()
