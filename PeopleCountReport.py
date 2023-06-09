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
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mysql.connector import connect, Error

LARGE_FONT = ("Verdana", 30, "bold")
NORMAL_FONT = ("Verdana", 15, "bold")
SMALL_FONT = ("Verdana", 9)

class PeopleCountReportPage(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        # tk.Tk.__init__(self, *args, **kwargs)
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.wm_title("People Statistic Report")
        self.iconbitmap(default="store_logo.ico")

        self.people_count_list = self.get_people_count_data()
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

    def get_people_count_data(self):
        people_count_list = []
        try:
            with connect(host="127.0.0.1", user="root", password="", database="smart_convenience_store") as connection:
                query = """
                    SELECT * FROM people_counting
                """
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    for row in results:
                        people_count = PeopleCount(*row)
                        people_count_list.append(people_count)
        except Error as e:
            print(e)
        return people_count_list

    def get_people_count_data_based_on_date(self):
        people_count_list = {"year": [], "month": [], "total": []}
        try:
            with connect(host="127.0.0.1", user="root", password="", database="smart_convenience_store") as connection:
                query = """
                    SELECT YEAR(date_time) as year, MONTH(date_time) as month, SUM(people_count) 
                    FROM people_counting 
                    GROUP BY year, month 
                    ORDER BY year, month
                """
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    for row in results:
                        people_count_list["year"].append(row[0])
                        people_count_list["month"].append(row[1])
                        people_count_list["total"].append(row[2])
        except Error as e:
            print(e)
        print(people_count_list)
        return people_count_list

    def create_report(self, parent):
        frame_selection = tk.Frame(parent)
        representation_label = tk.Label(frame_selection, text="People Statistic Information", font=("Verdana", 25, "bold"))
        representation_label.pack()

        option_label = tk.Label(frame_selection, text="Choose representation:", font=NORMAL_FONT)
        option_label.pack(side="top")
        
        option_cb = ttk.Combobox(frame_selection, values=("Table", "Graph"), state="readonly")
        option_cb.set("Table")
        option_cb.pack(side="top")

        frame_selection.pack(side="top", fill="x")

        self.frame_table = tk.Frame(parent)
        self.frame_table.pack(side="top", fill="both", expand=True)

        self.frame_graph = tk.Frame(parent)

        option_cb.bind("<<ComboboxSelected>>", self._selected_representation)

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

        columns = ('date', 'people_count')
        self.table = ttk.Treeview(parent, columns=columns, show="headings")
        self.table.heading("date", text="Date")
        self.table.heading("people_count", text="People Count")

        self.table.column("date", width=100, anchor="center")
        self.table.column("people_count", width=100, anchor="center")

        # self.table.bind("<<TreeviewSelect>>", self.item_selected)
        # self.table.bind("<Double-1>", self.item_selected)
        self.table.grid(row=0, column=0, sticky="nsew", pady=20, padx=(300,0))

        # add a scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="nwsw")

        for data in self.people_count_list:
            people_count_data = (data.date, data.count)
            self.table.insert("", tk.END, values=people_count_data)

    def _create_graph(self, parent):
        self.frame_table.pack_forget()
        parent.pack(side="top", fill="both", expand=True)

        month_map = {1: "Jan", 2: "Feb", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
                     8: "August", 9: "Sept", 10: "Oct", 11: "Nov", 12: "Dec"}
        people_date_month = []
        people_count_data = self.get_people_count_data_based_on_date()

        for year, month in zip(people_count_data["year"], people_count_data["month"]):
            date_month = month_map[month]
            date = str(year) + " " + date_month
            people_date_month.append(date) 

        f = Figure(figsize=(3,3), dpi=100)
        a = f.add_subplot(111)
       
        a.plot(people_date_month, people_count_data["total"], label="Amount(RM)", linestyle="solid")

        if not self.is_canvas_created:
            canvas = FigureCanvasTkAgg(f, parent)
            canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

            toolbar = NavigationToolbar2Tk(canvas, parent)
            toolbar.update()
            canvas._tkcanvas.pack(side="top", fill="both", expand=True)

class PeopleCount:
    def __init__(self, date, count):
        self.date = date
        self.count = count


if __name__ == "__main__":
    m = PeopleCountReportPage()
    m.show_page()