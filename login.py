from tkinter import *
from ldap_server import LdapServer

import admin_pwd as admin_pwd
import colors
from PIL import ImageTk, Image
from certificate_authority.ca_client import CaClient, handle_cert_local

from dotenv.main import load_dotenv
import os

load_dotenv()

CA_CLIENT_CERT_DIR = os.environ["CA_CLIENT_CERT_DIR"]


class LoginPage:
    def __init__(self, base=None):
        self.base = base

    def Login(self, event=None):
        self.error_label.place(relx=0.65, y=340, anchor=CENTER)
        if self.USERNAME.get() == "" or self.PASSWORD.get() == "":
            self.error_label.config(
                text="Please fill out both fields !!!", fg=colors.error, bg="#ff9966"
            )
        else:
            ldap_server = LdapServer(admin_pwd.LDAP_ADMIN_PWD)
            result = ldap_server.login(
                username=self.USERNAME.get(), password=self.PASSWORD.get()
            )
            if not result:
                handle_local = handle_cert_local(
                    CA_CLIENT_CERT_DIR + self.USERNAME.get() + "_cert.pem"
                )
                if not handle_local:
                    self.error_label.config(
                        text="no certificate issued",
                        fg=colors.error,
                        bg=colors.error_bg,
                    )
                else:

                    client = CaClient(self.USERNAME)
                    client.connect()
                    client.verify_cert()
                    if client.cert_is_ok == "Ok":
                        self.welcome()
                    else:
                        self.error_label.config(
                            text="Access denied,invalid certificate",
                            fg=colors.error,
                            bg=colors.error_bg,
                        )

            else:
                self.error_label.config(
                    text=result, fg=colors.error, bg=colors.error_bg
                )

    def signupPage(self):
        self.root.withdraw()
        self.root.destroy()

        from signup import Signup

        login = Signup()
        login.main()

    def welcome(self):
        self.root.withdraw()
        self.root.destroy()
        from welcome import Welcome

        w = Welcome(username=self.USERNAME.get())

    def clientInterface(self):

        self.root.withdraw()
        self.root.destroy()
        from client_inetrface import ChatInterface

        t = ChatInterface(username=self.USERNAME.get())

    # main frame
    def main(self):
        self.root = Toplevel(self.base)
        self.root.geometry("700x400")
        self.root.title("Login Form")
        self.root.config(bg=colors.login_bg)

        # data binding
        self.USERNAME = StringVar(self.root)
        self.PASSWORD = StringVar(self.root)

        # backround image
        img = Image.open("./assets/bg2.jpg").resize((700, 400))
        bg = ImageTk.PhotoImage(img)
        label = Label(self.root, image=bg)
        label.place(x=0, y=0)
        label.pack(fill=BOTH, expand=YES)

        # Page Title
        label_0 = Label(self.root, text="WeChat", width=40, font=("bold", 30))
        label_0.place(relx=0.5, y=20, anchor=CENTER)
        label_0.config(bg=colors.blue_light, fg=colors.blue_dark)

        # subtitle text
        label_login = Label(self.root, text="LOGIN", font=("bold", 20))
        label_login.place(relx=0.5, y=120, anchor=CENTER)
        label_login.config(bg=colors.blue_light, fg=colors.blue_2)

        # Username label & entry
        label_username = Label(
            self.root, width=10, text="Username :", font=("bold", 13)
        )
        label_username.place(relx=0.5, y=160, anchor=CENTER)
        label_username.config(bg=colors.blue_light, fg=colors.blue_dark)

        input_username = Entry(self.root, textvariable=self.USERNAME)
        input_username.place(relx=0.72, y=160, anchor=CENTER)
        input_username.config(
            bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg
        )

        # Password label & entry
        label_passwd = Label(self.root, width=10, text="Password :", font=("bold", 13))
        label_passwd.place(relx=0.5, y=210, anchor=CENTER)
        label_passwd.config(bg=colors.blue_light, fg=colors.blue_dark)

        input_passwd = Entry(self.root, textvariable=self.PASSWORD, show="*")
        input_passwd.place(relx=0.72, y=210, anchor=CENTER)
        input_passwd.config(
            bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg
        )

        # Submit button
        btn = Button(
            self.root,
            text="Submit",
            width=10,
            bg=colors.blue_dark,
            fg=colors.blue_dark,
            command=self.Login,
        )
        btn.place(relx=0.5, y=300, anchor=CENTER)

        btn.bind("<Return>", self.Login)
        btn.config(
            bg="#35a666",
            fg="#FFFFFF",
            activebackground="#0AAE2F",
            activeforeground=colors.blue_dark,
        )

        # Submit button
        btnlogin = Button(
            self.root,
            text="SignUp",
            width=10,
            bg=colors.blue_dark,
            fg=colors.blue_dark,
            command=self.signupPage,
        )
        btnlogin.place(relx=0.7, y=300, anchor=CENTER)

        btnlogin.bind("<Return>", self.signupPage)
        btnlogin.config(
            bg=colors.blue_dark,
            fg="#FFFFFF",
            activebackground=colors.blue_light,
            activeforeground=colors.blue_dark,
        )

        # Error label
        self.error_label = Label(self.root, width=30, font=("bold", 12))
        self.error_label.place(relx=0.65, y=440, anchor=CENTER)
        self.error_label.config(bg=colors.blue_light)

        self.root.resizable(0, 0)
        self.root.mainloop()
