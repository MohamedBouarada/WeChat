import tkinter as tk
from tkinter import *

import colors
from tkinter import Button, Frame, messagebox
import socket
import threading
from controller_message_format import ControllerMessageFormat
from receiver import Receiver, ReceiverRabbitMqConfigure

from sender import Sender, SenderRabbitmqConfigure

import colors

class Welcome:
    def __init__(self,root=None,username=''):
        
        self.root=root
        self.connected_users = []
        self.rooms = {'room1': [], 'room2': [], 'room3': [], 'room4': []}
        self.users_in_room=[]  
        self.num_room=''
        self.username = username
        
        controller_receiver_config = ReceiverRabbitMqConfigure(host='localhost',
                                                               queue='', 
                                                                exchange='controller_exchange', 
                                                                exchange_type='fanout', 
                                                                exclusive=False
                                                                )
        self.controller_receiver = Receiver(controller_receiver_config)
        self.controller_receiver.connect()

        controller_sender_config = SenderRabbitmqConfigure(queue='main_queue',
                                                           host='localhost',
                                                           routingKey='main_queue',
                                                           exchange='from_client_to_controller',
                                                           exchange_type='direct')
        self.controller_sender = Sender(controller_sender_config)
        self.controller_sender.connect()
        

        self.connect()
        self.main()
        message = ControllerMessageFormat(
            "onNewConnection", {"username": self.username})

        message.convertToString()
        self.controller_sender.send_message(message.msg)

    def main(self):
        
        self.root=Toplevel()  
        self.root.geometry('700x400')
        self.root.title("Login Form")
        self.root.config(bg=colors.login_bg)

        # Submit button
        self.btnlogin = Button(self.root, text='room1', width=15, bg=colors.blue_dark,fg=colors.blue_dark, command= lambda: self.enterRoom("room1"))
        self.btnlogin.place(relx=0.7, y=100,anchor=CENTER)

        self.btnlogin.bind('<Return>', (lambda event: self.enterRoom(room="room1")))
        self.btnlogin.config(bg=colors.blue_dark, fg="#FFFFFF",activebackground=colors.blue_light, activeforeground=colors.blue_dark)

        # Submit button
        self.btnlogin = Button(self.root, text='room2', width=15, bg=colors.blue_dark,fg=colors.blue_dark, command= lambda: self.enterRoom("room2"))
        self.btnlogin.place(relx=0.7, y=150,anchor=CENTER)

        self.btnlogin.bind('<Return>', (lambda event: self.enterRoom(room="room2")))
        self.btnlogin.config(bg=colors.blue_dark, fg="#FFFFFF",activebackground=colors.blue_light, activeforeground=colors.blue_dark)

        self.btnlogin = Button(self.root, text='room3', width=15, bg=colors.blue_dark,fg=colors.blue_dark, command= lambda: self.enterRoom("room3"))
        self.btnlogin.place(relx=0.7, y=250,anchor=CENTER)

        self.btnlogin.bind('<Return>', (lambda event: self.enterRoom(room="room3")))
        self.btnlogin.config(bg=colors.blue_dark, fg="#FFFFFF",activebackground=colors.blue_light, activeforeground=colors.blue_dark)

        # Submit button
        self.btnlogin = Button(self.root, text='room4', width=15, bg=colors.blue_dark,fg=colors.blue_dark, command= lambda: self.enterRoom("room4"))
        self.btnlogin.place(relx=0.7, y=300,anchor=CENTER)

        self.btnlogin.bind('<Return>',(lambda event: self.enterRoom(room="room4")))
        self.btnlogin.config(bg=colors.blue_dark, fg="#FFFFFF",activebackground=colors.blue_light, activeforeground=colors.blue_dark)

        # it is use for display the registration form on the window
        self.root.resizable(0, 0)
        self.root.mainloop()
        print("Welcome WeChat :)")




    def enterRoom(self,room):
        self.num_room=room
        message = ControllerMessageFormat(
            "onRoomEnter", {"username": self.username,"room":room})

        message.convertToString()
        self.controller_sender.send_message(message.msg)

    def leaveRoom(self,room):
        message = ControllerMessageFormat(
            "onRoomLeave", {"username": self.username,"room":room})

        message.convertToString()
        self.controller_sender.send_message(message.msg)    

    def connect(self):
        global client
        print(self.username)
        self.connect_to_server(self.username)
        

    def print_success(self, *args):
        print("success")
        print(args)

    def connect_to_server(self, name):
        global client, HOST_PORT, HOST_ADDR
        try:
            
            # threading._start_new_thread(
            #     self.receive_message_from_server, ("client",))
            threading._start_new_thread(
                self.receive_message_from_controller, ("client",))
        except Exception as e:
            print(e)
            tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR +
                                    " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")

    def receive_message_from_controller(self, c):
        def callback(ch, method, properties, body):
            print("new connection", body)
            message = ControllerMessageFormat()
            message.convertToJson(body.decode())
            print('actionnnnn:::::::',message.action,':::::::::',message.data)
            self.handleAction(message.action, message.data)
            # ch.basic_ack(delivery_tag=method.delivery_tag)
        while True:
            print("in loop")
            self.controller_receiver.listen_channel(callback)

    # def receive_message_from_server(self, c):
    #     self.msg = ''

    #     def callback(ch, method, properties, body):
    #         message = ControllerMessageFormat()
    #         message.convertToJson(body.decode())
    #         self.handleAction(message.action, message.data)

    #         print('in', body)
    #         self.msg = body
    #         # ch.basic_ack(delivery_tag=method.delivery_tag)
    #         texts = self.tkDisplay.get("1.0", tk.END).strip()
    #         self.tkDisplay.config(state=tk.NORMAL)
    #         if len(texts) < 1:
    #             self.tkDisplay.insert(tk.END, self.msg.decode())
    #         else:
    #             self.tkDisplay.insert(tk.END, "\n\n"+self.msg.decode())

    #         self.tkDisplay.config(state=tk.DISABLED)
    #         self.tkDisplay.see(tk.END)

    #     while True:
    #         # from_server = sck.recv(4096).decode()
    #         print('befoooooooooooooooree')
    #         self.receiver.listen_channel(callback)
    #         # if not from_server: break

    #         print('out', self.msg)
            

    def handleAction(self,action,data):
        if action == "connected":
            self.connected_users=data["connected_users"]
            print("aAAAAAAAAAHLAAAAAAAAAAAAAAAAAAAAAA")
            self.rooms=data['rooms']
            #todo later

            
        elif action == "joined":
            print('d5alt joiiiiiindedddd')
            self.users_in_room=data['users_in_room']
            if data['current']==self.username:
                self.clientInterface()

    def clientInterface(self):
        print("d5altttttttttttttttttttttttttt")
        self.root.withdraw()
        # self.root.destroy()
        from client_inetrface import ChatInterface
        
        # self.root.destroy()
        t=ChatInterface(username=self.username,num_room=self.num_room,users_in_room=self.users_in_room)
        print("5raaaaaaaaaajjjjjjjjt")
    def home(self):
        
        self.root.withdraw()
        self.root.destroy()
        from home import HomePage
        
        # self.root.destroy()
        t=HomePage()
        t.main()