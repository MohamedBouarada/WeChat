from tkinter import *

import colors
from PIL import ImageTk, Image


class HomePage:
    def __init__(self, root=None):
        self.root = root

    def signupPage(self):
        self.root.withdraw()

        from signup import Signup

        login = Signup(base=self.root)
        login.main()

    def loginPage(self):
        self.root.withdraw()
        from login import LoginPage

        login = LoginPage(base=self.root)
        login.main()

    # main frame
    def main(self):

        self.root = Tk()
        self.canvas = Canvas(self.root, width=700, height=400)
        self.canvas.pack()
        IMAGE_PATH = "./assets/bg2.jpg"
        self.img = ImageTk.PhotoImage(
            Image.open(IMAGE_PATH).resize((700, 400), Image.ANTIALIAS)
        )
        self.canvas.background = self.img
        self.bg = self.canvas.create_image(0, 0, anchor=NW, image=self.img)

        # Page Title
        label_0 = Label(self.root, text="WeChat", width=40, font=("bold", 30))
        label_0.place(relx=0.5, y=20, anchor=CENTER)
        label_0.config(bg=colors.blue_light, fg=colors.blue_dark)

        # Submit button
        btnlogin = Button(
            self.root,
            text="SignUp",
            width=15,
            bg=colors.blue_dark,
            fg=colors.blue_dark,
            command=self.signupPage,
        )
        btnlogin.place(relx=0.7, y=170, anchor=CENTER)

        btnlogin.bind("<Return>", self.signupPage)
        btnlogin.config(
            bg=colors.blue_dark,
            fg="#FFFFFF",
            activebackground=colors.blue_light,
            activeforeground=colors.blue_dark,
        )

        # Submit button
        btnlogin = Button(
            self.root,
            text="Login",
            width=15,
            bg=colors.blue_dark,
            fg=colors.blue_dark,
            command=self.loginPage,
        )
        btnlogin.place(relx=0.7, y=220, anchor=CENTER)

        btnlogin.bind("<Return>", self.loginPage)
        btnlogin.config(
            bg=colors.blue_dark,
            fg="#FFFFFF",
            activebackground=colors.blue_light,
            activeforeground=colors.blue_dark,
        )

        # it is use for display the registration form on the window
        self.root.resizable(0, 0)
        self.root.mainloop()


s = HomePage()
s.main()
