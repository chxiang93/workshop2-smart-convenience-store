# Workshop 2 Group 3
# Group Members:
# 1) Sue Chen Xiang B032010034
# 2. Fatin Najdah binti Najmi Ismail B032010201 
# 3. Nur Afiqah binti Anuar B032010114 
# 4. Ken Prameswari Caesarella B032010461 
# 5. Mohammad Irsyad bin Mohd Shahril B032010242

import tkinter as tk
import cv2 
from PIL import ImageTk, Image
from tkinter.messagebox import askokcancel
from mysql.connector import connect, Error
from HomePage import HomePage

LARGE_FONT = ("Verdana", 30, "bold")
NORMAL_FONT = ("Verdana", 15, "bold")
SMALL_FONT = ("Verdana", 12)

class LoginPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Login Page")
        self.iconbitmap(default="store_logo.ico")
        self.wm_protocol("WM_DELETE_WINDOW", self.on_closing)

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
        frame_mainmenu.grid_rowconfigure(0, weight=1)
        frame_mainmenu.grid_columnconfigure(0, weight=1)
        frame_mainmenu.grid_columnconfigure(1, weight=1)

        img = cv2.imread("store_logo.png", cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (400,400))
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        logo = tk.Label(frame_mainmenu, image=img, background="#FFD553")
        logo.grid(row=0, column=0, sticky="nsew")
        logo.img = img

        frame_login = tk.Frame(frame_mainmenu, background="#EDEDED", relief="solid", borderwidth=3)
        frame_login.grid(row=0, column=1, sticky="nsew", padx=(30,50), pady=40)

        for i in range(4):
            frame_login.grid_rowconfigure(i, weight=1)
            if i >= 2:
                continue
            frame_login.grid_columnconfigure(i, weight=1)
            
        login_label = tk.Label(frame_login, text="Sign In", font=LARGE_FONT)
        login_label.grid(row=0, column=0, columnspan=2, sticky="nwne")

        username_label = tk.Label(frame_login, text="Username:", font=SMALL_FONT)
        username_label.grid(row=1, column=0, sticky="nwne", padx=(20,0), pady=20)

        self.username_entry = tk.Entry(frame_login, font=SMALL_FONT)
        self.username_entry.grid(row=1, column=1, sticky="nwne", padx=20, pady=20)

        password_label = tk.Label(frame_login, text="Password:", font=SMALL_FONT)
        password_label.grid(row=2, column=0, sticky="nwne", padx=(20,0), pady=10)

        self.password_entry = tk.Entry(frame_login, font=SMALL_FONT, show="*")
        self.password_entry.grid(row=2, column=1, sticky="nwne", padx=20, pady=10)
        self.password_entry.bind("<Return>", self.login)

        self.error_label = tk.Label(frame_login, background="#EDEDED", foreground="red")
        self.error_label.grid(row=3, column=0, sticky="ne", padx=(20,0), pady=(0, 30))

        login_button = tk.Button(
            frame_login, 
            text="Login", 
            background="#FFD553", 
            activebackground="yellow", 
            relief="solid", 
            borderwidth=2, 
            width=10, 
            height=2, 
            command=self.login
        )
        login_button.grid(row=3, column=1, sticky="ne", padx=20, pady=(0, 30))

    def show_page(self):
        self.geometry("900x500")
        self.mainloop()

    def login(self, event=None):
        admin_list = self.get_admin_data()
        username = self.username_entry.get()
        password = self.password_entry.get()

        for admin in admin_list:
            if username == admin.username and password == admin.password:
                self.error_label.configure(text="")
                self.destroy()
                HomePage().show_page()
            else:
                self.error_label.configure(text="The username or \npassword is incorrect!!!")

    def get_admin_data(self):
        admin_list = []
        try:
            with connect(host="127.0.0.1", user="root", password="", database="smart_convenience_store") as connection:
                query = """
                    SELECT username, password FROM ADMIN
                """
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    for row in results:
                        print(*row)
                        product = Admin(*row)
                        admin_list.append(product)
        except Error as e:
            print(e)
        return admin_list

    def on_closing(self):
        if askokcancel(title="Exit System", message="Are you sure you want to exit the system?"):
            self.destroy()

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

if __name__ == "__main__":
    app = LoginPage()
    app.show_page()
