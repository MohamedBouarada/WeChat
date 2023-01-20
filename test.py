import tkinter as tk
from tkinter import *

import colors
from tkinter import Button, Frame, messagebox
class Chat(Frame):
    def __init__(self, master=None, username='',num_room='',users_in_room=[]):
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.window = tk.Tk()
        
        self.window.title("Client")
        self.username = username

        self.connected_users = []
        self.rooms = {'room1': [], 'room2': [], 'room3': [], 'room4': []}
        self.users_in_room=users_in_room  
        self.num_room=num_room

        

        

        self.window.geometry('800x500')
        self.window.title("WeChat")
        self.window.config(background=colors.blue_dark)

        # self.topFrame = tk.Frame(self.window)
        # # self.lblName = tk.Label(self.topFrame, text = "Name:").pack(side=tk.LEFT)
        # # self.entName = tk.Entry(self.topFrame)
        # # self.entName.pack(side=tk.LEFT)
        # # self.btnConnect = tk.Button(self.topFrame, text="Connect", command=lambda : self.connect())
        # # self.btnConnect.pack(side=tk.LEFT)
        # # btnConnect.bind('<Button-1>', connect)
        # # self.btnlogin = Button(self.window, text='Room1', width=15, bg=colors.blue_dark,fg=colors.blue_dark, command= lambda: self.enterRoom("room1"))
        # # self.btnlogin.place(relx=0, y=2,anchor=CENTER)

        # # self.btnlogin.bind('<Return>',(lambda event: self.enterRoom(room="room1")))
        # # self.btnlogin.config(bg=colors.blue_dark, fg="#FFFFFF",activebackground=colors.blue_light, activeforeground=colors.blue_dark)

        # # leave button
        # self.btnlogin = Button(self.topFrame, text='Leave Room', width=15, bg=colors.blue_dark,fg=colors.blue_dark, command= lambda: self.leaveRoom())
        # # self.btnlogin.place(relx=0.5, y=102,anchor=CENTER)
        # self.btnlogin.pack(side=tk.LEFT)

        # self.btnlogin.bind('<Return>',(lambda event: self.leaveRoom()))
        # self.btnlogin.config(bg=colors.blue_dark, fg="#FFFFFF",activebackground=colors.blue_light, activeforeground=colors.blue_dark)

        # self.topFrame.pack(side=tk.TOP)

        # self.clientFrame = tk.Frame(self.window)
        # self.lblLine = tk.Label(self.clientFrame, text="**********Client List**********").pack()
        # self.scrollBar = tk.Scrollbar(self.clientFrame)
        # self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        # self.tkDisplay = tk.Text(self.clientFrame, height=15, width=30)
        # self.tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        # self.scrollBar.config(command=self.tkDisplay.yview)
        # self.tkDisplay.config(yscrollcommand=self.scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
        # self.clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

        # # leave button
        # self.btnlogin = Button(self.topFrame, text='Leave Room', width=15, bg=colors.blue_dark,fg=colors.blue_dark, command= lambda: self.leaveRoom())
        # # self.btnlogin.place(relx=0.5, y=102,anchor=CENTER)
        # self.btnlogin.pack(side=tk.LEFT)

        # self.btnlogin.bind('<Return>',(lambda event: self.leaveRoom()))
        # self.btnlogin.config(bg=colors.blue_dark, fg="#FFFFFF",activebackground=colors.blue_light, activeforeground=colors.blue_dark)




        self.leftFrame = tk.Frame(self.window,background="white" )
        self.listTitle=Label(self.leftFrame, text="Chat List",font=('times new roman', 20))
        self.listTitle.config(fg="white",bg=colors.success_bg,width=15)
        self.listTitle.pack()
        self.liste = Listbox(self.leftFrame,width=25,height=22, bg='white',fg=colors.blue_1)
        self.liste.insert(1, "Mohamed","aaaaaaaaaaaaaaaaaa")
        self.liste.insert(2, "Racem")
        self.liste.insert(3, "La7nach")
        self.liste.insert(4, "Zaaaab")
        self.liste.insert(5, "3asba")
    
        self.liste.pack()

        self.leaveBtn = Button(self.leftFrame, text='Leave Room',width=10 ,font=('bold', 15), bg=colors.blue_dark,fg=colors.blue_dark, command= lambda: self.leaveRoom())
        # self.leaveBtn.place(relx=0.5, y=102,anchor=CENTER)
        self.leaveBtn.pack(padx=(1, 1),pady=(1, 1))

        self.leaveBtn.bind('<Return>',(lambda event: self.leaveRoom()))
        self.leaveBtn.config(bg=colors.blue_dark, fg="#FFFFFF",activebackground=colors.blue_light, activeforeground=colors.blue_dark)

        self.leftFrame.pack(side=tk.LEFT ,padx=(20, 20),pady=(20,20))




        self.displayFrame = tk.Frame(self.window,bg=colors.blue_3,width=400)
        self.lblLine = tk.Label(
            self.displayFrame, text="ROOOOM1",bg=colors.blue_3,fg=colors.blue_dark,font=('times new roman', 22)).pack()
        
        self.scrollBar = tk.Scrollbar(self.displayFrame,bg=colors.blue_2,activebackground=colors.blue_1)
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tkDisplay = tk.Text(self.displayFrame, height=21, width=55,bg=colors.blue_3)
        self.tkDisplay.pack(side=tk.TOP, fill=tk.Y, padx=(5, 13))
        self.tkDisplay.tag_config("tag_your_message", foreground="blue")
        self.scrollBar.config(command=self.tkDisplay.yview)
        self.tkDisplay.config(yscrollcommand=self.scrollBar.set,
                              background="white", highlightbackground=colors.blue_light, state="disabled")
        

        self.bottomFrame = tk.Frame(self.displayFrame,bg=colors.blue_3)
        self.tkMessage = tk.Text(self.bottomFrame, height=2, width=55)
        self.tkMessage.pack(side=tk.BOTTOM, padx=(5, 13), pady=(5, 10))
        self.tkMessage.config(highlightbackground="grey", state="normal",fg=colors.blue_dark)
        self.tkMessage.bind("<Return>", (lambda event: self.getChatMessage(
            self.tkMessage.get("1.0", tk.END))))
        self.bottomFrame.pack(side=tk.BOTTOM)

        self.displayFrame.pack(side=tk.LEFT)

        
        self.window.resizable(0, 0)
        self.window.mainloop()



t=Chat()