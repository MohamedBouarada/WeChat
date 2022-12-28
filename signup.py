from tkinter import *
from ldap_server import LdapServer
import time
import admin_pwd
import colors
from PIL import ImageTk, Image  


class Signup:

    def Register(self, event=None):
        self.error_label.place(relx=0.65, y=385,anchor=CENTER)
        if self.USERNAME.get() == "" or self.PASSWORD.get() == "" or self.EMAIL.get() == "" or self.UID.get() == "":
            self.error_label.config(
                text="Please fill out all fields !!!", fg=colors.error, bg="#ff9966")

        else:
            # user object
            user_obj = {
                'username': self.USERNAME.get(),
                'password': self.PASSWORD.get(),
                'email': self.EMAIL.get(),
                'gender': self.GENDER.get(),
                'group_id': 5000,  
                'uid': self.UID.get()  # student id
            }
            
            ldap_s = LdapServer(admin_pwd.LDAP_ADMIN_PWD)
            result = ldap_s.register(user_obj)
            print(result)
            if not result:
                self.HomeWindow()
                self.error_label.config(text="Sucess", fg=colors.success, bg=colors.success_bg)
            else:
                self.error_label.config(text=result, fg=colors.error, bg=colors.error_bg)

    def HomeWindow(self):
        self.root.withdraw()
        global Home
        Home = Toplevel()
        Home.title("WeChat")
        width = 600
        height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.root.resizable(0, 0)
        Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
        lbl_home = Label(Home, text="Successfully Login!",font=('times new roman', 20)).pack()
        btn_back = Button(Home, text='Back', command=self.Back).pack(pady=20, fill=X)

    
    
    def Back(self):
        Home.destroy()
        self.root.deiconify()

    def main(self):
        # main frame
        self.root = Tk()
        self.root.geometry('700x400')
        self.root.title("Signup Form")
        self.root.config(bg=colors.login_bg)

        # data binding
        self.USERNAME = StringVar(self.root)
        self.EMAIL = StringVar(self.root)
        self.PASSWORD = StringVar(self.root)
        self.GENDER = StringVar(self.root)
        self.UID = StringVar(self.root)
        
        # backround image
        img =Image.open('/home/mohamed/GL4/WeChat/assets/bg2.jpg').resize((700,400))
        bg = ImageTk.PhotoImage(img)
        label = Label(self.root, image=bg )
        label.place(x = 0,y = 0)
        label.pack(fill=BOTH, expand=YES)

        # Page Title
        label_title = Label(self.root, text="WeChat", width=40, font=("bold", 30))
        label_title.place(relx=0.5, y=20,anchor=CENTER)
        label_title.config(bg=colors.blue_light, fg=colors.blue_dark)

        # Registration form
        label_signup = Label(self.root,text="SIGNUP",  font=("bold", 20))
        label_signup.place(relx=0.5, y=100,anchor=CENTER)
        label_signup.config(bg=colors.blue_light, fg=colors.blue_2)

        # UserName label & entry
        label_username = Label(self.root, width=10,text="Username :",  font=("bold", 13))
        label_username.place(relx=0.5, y=140,anchor=CENTER)
        label_username.config(bg=colors.blue_light, fg=colors.blue_dark)

        input_username = Entry(self.root, textvariable=self.USERNAME)
        input_username.place(relx=0.72, y=140,anchor=CENTER)
        input_username.config(bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg)
        

        # self.EMAIL label & entry
        label_email = Label(self.root, width=10,text="Email :",  font=("bold", 13))
        label_email.place(relx=0.5, y=180,anchor=CENTER)
        label_email.config(bg=colors.blue_light, fg=colors.blue_dark)  
        
        input_email = Entry(self.root, textvariable=self.EMAIL)
        input_email.place(relx=0.72, y=180,anchor=CENTER)
        input_email.config(bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg)
        

        # self.PASSWORD label & entry
        label_passwd = Label(self.root,width=10, text="Password :", font=("bold", 13))
        label_passwd.place(relx=0.5, y=220,anchor=CENTER)
        label_passwd.config(bg=colors.blue_light, fg=colors.blue_dark)

        input_passwd = Entry(self.root, textvariable=self.PASSWORD, show="*")
        input_passwd.place(relx=0.72, y=220,anchor=CENTER)
        input_passwd.config(bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg)
        

        # self.GENDER label & radio-box
        label_gender = Label(self.root, width=10,text="Gender :",  font=("bold", 13))
        label_gender.place(relx=0.5, y=260,anchor=CENTER)
        label_gender.config(bg=colors.blue_light, fg=colors.blue_dark)

        optionMale = Radiobutton(self.root, text="Male", variable=self.GENDER,value=1)
        optionMale.place(relx=0.6, y=250)
        optionFemale = Radiobutton(self.root, text="Female",variable=self.GENDER, value=2)
        optionFemale.place(relx=0.7, y=250)
        optionFemale.config(bg=colors.input_bg, fg=colors.blue_dark)
        optionMale.config(bg=colors.input_bg, fg=colors.blue_dark)

        # Student Id label & entry
        label_StudentId = Label(self.root, width=10,text="Student Id :",  font=("bold", 13))
        label_StudentId.place(relx=0.5, y=300,anchor=CENTER)
        label_StudentId.config(bg=colors.blue_light, fg=colors.blue_dark)

        input_StudentId = Entry(self.root, textvariable=self.UID)
        input_StudentId.place(relx=0.72, y=300,anchor=CENTER)
        input_StudentId.config(bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg)


        # Error label
        self.error_label = Label(self.root,width=30,  font=("bold", 12))
        self.error_label.place(relx=0.65, y=440,anchor=CENTER)
        self.error_label.config(bg=colors.blue_light)

        # Submit button
        btn = Button(self.root, text='Submit', width=10, bg=colors.blue_dark,fg=colors.blue_dark, command=self.Register)
        btn.place(relx=0.5, y=340,anchor=CENTER)

        btn.bind('<Return>', self.Register)
        btn.config(bg=colors.blue_dark, fg="#FFFFFF",activebackground="#35a666", activeforeground=colors.blue_dark)
        

        
        self.root.mainloop()
        print("Signup :)")


s = Signup()
s.main()