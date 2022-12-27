from tkinter import *
from ldap_server import LdapServer
import time
import admin_pwd
import colors
from PIL import ImageTk, Image  

def Login(event=None):
    error_label.place(relx=0.65, y=340,anchor=CENTER)
    if USERNAME.get() == "" or PASSWORD.get() == "":
        error_label.config(
            text="Please fill out both fields !!!", fg=colors.error, bg="#ff9966")
    else:
        ldap_s = LdapServer(admin_pwd.LDAP_ADMIN_PWD)
        result = ldap_s.login(username=USERNAME.get(), password=PASSWORD.get())
        if not result:
            # HomeWindow()
            USERNAME.set("")
            PASSWORD.set("")
            error_label.config(text="Sucess", fg=colors.success, bg=colors.success_bg)

        else:
            error_label.config(text=result, fg=colors.error, bg=colors.error_bg)


def HomeWindow():
    global Home
    root.withdraw()
    Home = Toplevel()
    Home.title("WeChat")
    width = 600
    height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.resizable(0, 0)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    lbl_home = Label(Home, text="Successfully Login!",font=('times new roman', 20)).pack()
    btn_back = Button(Home, text='Back', command=Back).pack(pady=20, fill=X)


def Back():
    Home.destroy()
    root.deiconify()

# main frame
root = Tk()
root.geometry('700x400')
root.title("Login Form")
root.config(bg=colors.login_bg)


# data binding
USERNAME = StringVar(root)
PASSWORD = StringVar(root)

# backround image
img =Image.open('/home/mohamed/GL4/WeChat/assets/bg2.jpg').resize((700,400))
bg = ImageTk.PhotoImage(img)
label = Label(root, image=bg )
label.place(x = 0,y = 0)
label.pack(fill=BOTH, expand=YES)


# Login Title
label_0 = Label(root, text="WeChat", width=40, font=("bold", 30))
label_0.place(relx=0.5, y=20,anchor=CENTER)
label_0.config(bg=colors.blue_light, fg=colors.blue_dark)

# subtitle text
label_login = Label(root,text="LOGIN",  font=("bold", 20))
label_login.place(relx=0.5, y=120,anchor=CENTER)
label_login.config(bg=colors.blue_light, fg=colors.blue_2)

# Username label & entry
label_username = Label(root, width=10,text="Username :",  font=("bold", 13))
label_username.place(relx=0.5, y=160,anchor=CENTER)
label_username.config(bg=colors.blue_light, fg=colors.blue_dark)

input_username = Entry(root, textvariable=USERNAME)
input_username.place(relx=0.72, y=160,anchor=CENTER)
input_username.config(bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg)

# Password label & entry
label_passwd = Label(root,width=10, text="Password :", font=("bold", 13))
label_passwd.place(relx=0.5, y=210,anchor=CENTER)
label_passwd.config(bg=colors.blue_light, fg=colors.blue_dark)

input_passwd = Entry(root, textvariable=PASSWORD, show="*")
input_passwd.place(relx=0.72, y=210,anchor=CENTER)
input_passwd.config(bg=colors.input_bg, fg=colors.blue_dark, insertbackground=colors.input_bg)

# Submit button
btn = Button(root, text='Submit', width=10, bg=colors.blue_dark,fg=colors.blue_dark, command=Login)
btn.place(relx=0.5, y=300,anchor=CENTER)

btn.bind('<Return>', Login)
btn.config(bg=colors.blue_dark, fg="#FFFFFF",activebackground="#35a666", activeforeground=colors.blue_dark)

# Error label
error_label = Label(root,width=30,  font=("bold", 12))
error_label.place(relx=0.65, y=440,anchor=CENTER)
error_label.config(bg=colors.blue_light)






# def resize_image(e):
#     global img,bg,label
#     root.resizable()
#     img =Image.open('/home/mohamed/GL4/WeChat/assets/chatBg.jpg').resize((e.width, e.height))
#     bg = ImageTk.PhotoImage(img)
#     label = Label(root, image=bg )
#     label.place(x = 0,y = 0)
#     label.pack(fill=BOTH, expand=YES)

# root.bind("<Configure>", resize_image)


# it is use for display the registration form on the window
root.resizable(0, 0)
root.mainloop()
print("login form successfully created :)")