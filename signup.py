from tkinter import *
from ldap_server import LdapServer
import time
import admin_pwd as admin_pwd
import colors
from PIL import ImageTk, Image
import re
from certificate_authority.ca_client import CaClient, handle_cert_local

from dotenv.main import load_dotenv
import os

load_dotenv()

CA_CLIENT_PATH = os.environ["CA_CLIENT_CERT_DIR"]


class Signup:
    def __init__(self, base=None):
        self.base = base

    def check(self):
        if re.match("[^@]+@[^@]+\.[^@]+", self.EMAIL.get()):
            return True
        else:
            return False

    def Register(self, event=None):
        self.error_label.place(relx=0.65, y=385, anchor=CENTER)
        if (
            self.USERNAME.get() == ""
            or self.PASSWORD.get() == ""
            or self.EMAIL.get() == ""
            or self.UID.get() == ""
        ):
            self.error_label.config(
                text="Please fill out all fields !!!", fg=colors.error, bg="#ff9966"
            )

        else:
            if not self.check():
                self.error_label.config(
                    text="Invalid Email !!!", fg=colors.error, bg="#ff9966"
                )
            else:
                # user object
                user_obj = {
                    "username": self.USERNAME.get(),
                    "password": self.PASSWORD.get(),
                    "email": self.EMAIL.get(),
                    "firstname": self.FIRSTNAME.get(),
                    "lastname": self.LASTNAME.get(),
                    "group_id": 5000,
                    "uid": self.UID.get(),  # student id
                }

                ldap_s = LdapServer(admin_pwd.LDAP_ADMIN_PWD)
                result = ldap_s.register(user_obj)
                if not result:
                    client = CaClient(self.USERNAME)
                    client.connect()
                    client.request_cert()
                    result = handle_cert_local(
                        CA_CLIENT_PATH + self.USERNAME.get() + "_cert.pem"
                    )
                    self.loginPage()
                    self.error_label.config(
                        text="Sucess", fg=colors.success, bg=colors.success_bg
                    )

                else:
                    self.error_label.config(
                        text=result, fg=colors.error, bg=colors.error_bg
                    )

    def loginPage(self):
        self.root.withdraw()
        self.root.destroy()

        from login import LoginPage

        login = LoginPage()
        # self.root.destroy()
        login.main()

    def main(self):
        # main frame
        self.root = Toplevel(self.base)
        self.root.geometry("700x400")
        self.root.title("Signup Form")
        self.root.config(bg=colors.login_bg)

        self.USERNAME = StringVar(self.root)
        self.EMAIL = StringVar(self.root)
        self.PASSWORD = StringVar(self.root)
        self.GENDER = StringVar(self.root)
        self.UID = StringVar(self.root)
        self.FIRSTNAME = StringVar(self.root)
        self.LASTNAME = StringVar(self.root)

        # backround image
        self.img = Image.open("./assets/bg2.jpg").resize((700, 400))
        self.bg = ImageTk.PhotoImage(self.img)
        label = Label(self.root, image=self.bg)
        label.place(x=0, y=0)
        label.pack(fill=BOTH, expand=YES)

        # Page Title
        label_title = Label(self.root, text="WeChat", width=40, font=("bold", 30))
        label_title.place(relx=0.5, y=20, anchor=CENTER)
        label_title.config(bg=colors.blue_light, fg=colors.blue_dark)

        # Registration form
        label_signup = Label(self.root, text="SIGNUP", font=("bold", 20))
        label_signup.place(relx=0.22, y=100, anchor=CENTER)
        label_signup.config(bg=colors.blue_light, fg=colors.blue_2)

        # self.FirstName label & entry
        label_firstname = Label(
            self.root, width=10, text="Firstname :", font=("bold", 13)
        )
        label_firstname.place(relx=0.5, y=100, anchor=CENTER)
        label_firstname.config(bg=colors.blue_light, fg=colors.blue_dark)

        input_firstname = Entry(self.root, textvariable=self.FIRSTNAME)
        input_firstname.place(relx=0.72, y=100, anchor=CENTER)
        input_firstname.config(
            bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg
        )

        # LastName label & entry
        label_lastname = Label(
            self.root, width=10, text="Lastname :", font=("bold", 13)
        )
        label_lastname.place(relx=0.5, y=140, anchor=CENTER)
        label_lastname.config(bg=colors.blue_light, fg=colors.blue_dark)

        input_lastname = Entry(self.root, textvariable=self.LASTNAME)
        input_lastname.place(relx=0.72, y=140, anchor=CENTER)
        input_lastname.config(
            bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg
        )

        # UserName label & entry
        label_username = Label(
            self.root, width=10, text="Username :", font=("bold", 13)
        )
        label_username.place(relx=0.5, y=180, anchor=CENTER)
        label_username.config(bg=colors.blue_light, fg=colors.blue_dark)

        input_username = Entry(self.root, textvariable=self.USERNAME)
        input_username.place(relx=0.72, y=180, anchor=CENTER)
        input_username.config(
            bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg
        )

        # self.EMAIL label & entry
        label_email = Label(self.root, width=10, text="Email :", font=("bold", 13))
        label_email.place(relx=0.5, y=220, anchor=CENTER)
        label_email.config(bg=colors.blue_light, fg=colors.blue_dark)

        input_email = Entry(self.root, textvariable=self.EMAIL)
        input_email.place(relx=0.72, y=220, anchor=CENTER)
        input_email.config(
            bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg
        )

        # self.PASSWORD label & entry
        label_passwd = Label(self.root, width=10, text="Password :", font=("bold", 13))
        label_passwd.place(relx=0.5, y=260, anchor=CENTER)
        label_passwd.config(bg=colors.blue_light, fg=colors.blue_dark)

        input_passwd = Entry(self.root, textvariable=self.PASSWORD, show="*")
        input_passwd.place(relx=0.72, y=260, anchor=CENTER)
        input_passwd.config(
            bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg
        )

        # Student Id label & entry
        label_StudentId = Label(
            self.root, width=10, text="Student Id :", font=("bold", 13)
        )
        label_StudentId.place(relx=0.5, y=300, anchor=CENTER)
        label_StudentId.config(bg=colors.blue_light, fg=colors.blue_dark)

        input_StudentId = Entry(self.root, textvariable=self.UID)
        input_StudentId.place(relx=0.72, y=300, anchor=CENTER)
        input_StudentId.config(
            bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg
        )

        # Error label
        self.error_label = Label(self.root, width=30, font=("bold", 12))
        self.error_label.place(relx=0.65, y=440, anchor=CENTER)
        self.error_label.config(bg=colors.blue_light)

        # Submit button
        btn = Button(
            self.root,
            text="Submit",
            width=10,
            bg=colors.blue_dark,
            fg=colors.blue_dark,
            command=self.Register,
        )
        btn.place(relx=0.5, y=340, anchor=CENTER)

        btn.bind("<Return>", self.Register)
        btn.config(
            bg="#35a666",
            fg="#FFFFFF",
            activebackground="#0AAE2F",
            activeforeground=colors.blue_dark,
        )

        # Submit button
        btnlogin = Button(
            self.root,
            text="Login",
            width=10,
            bg=colors.blue_dark,
            fg=colors.blue_dark,
            command=self.loginPage,
        )
        btnlogin.place(relx=0.7, y=340, anchor=CENTER)

        btnlogin.bind("<Return>", self.loginPage)
        btnlogin.config(
            bg=colors.blue_dark,
            fg="#FFFFFF",
            activebackground=colors.blue_light,
            activeforeground=colors.blue_dark,
        )

        self.root.mainloop()
