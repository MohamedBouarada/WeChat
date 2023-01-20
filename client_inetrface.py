import tkinter as tk
from tkinter import *

import colors
from tkinter import Button, Frame, messagebox
import socket
import threading
from controller_message_format import ControllerMessageFormat
from receiver import Receiver, ReceiverRabbitMqConfigure

from sender import Sender, SenderRabbitmqConfigure

# network client
client = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080


class ChatInterface(Frame):
    def __init__(self, master=None, username='',num_room='',users_in_room=[]):
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        self.window = tk.Tk()
        
        self.window.title("Client")
        self.username = username

        self.connected_users = []
        self.rooms = {'room1': [], 'room2': [], 'room3': [], 'room4': []}
        self.users_in_room=users_in_room  
        self.num_room=num_room

        server = SenderRabbitmqConfigure(queue='hello',
                                         host='localhost',
                                         routingKey='hello',
                                         exchange=self.num_room)
        serverconfigure = ReceiverRabbitMqConfigure(host='localhost',
                                                    queue='', exchange=self.num_room)
        self.sender = Sender(server)
        self.sender.connect()
        self.receiver = Receiver(config=serverconfigure)
        self.receiver.connect()
        
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
        message = ControllerMessageFormat(
            "onNewConnection", {"username": self.username})

        message.convertToString()
        self.controller_sender.send_message(message.msg)


        



        self.topFrame = tk.Frame(self.window)
        # self.lblName = tk.Label(self.topFrame, text = "Name:").pack(side=tk.LEFT)
        # self.entName = tk.Entry(self.topFrame)
        # self.entName.pack(side=tk.LEFT)
        # self.btnConnect = tk.Button(self.topFrame, text="Connect", command=lambda : self.connect())
        # self.btnConnect.pack(side=tk.LEFT)
        # btnConnect.bind('<Button-1>', connect)
        self.btnlogin = Button(self.window, text='Room1', width=15, bg=colors.blue_dark,fg=colors.blue_dark, command= lambda: self.enterRoom("room1"))
        self.btnlogin.place(relx=0, y=2,anchor=CENTER)

        self.btnlogin.bind('<Return>',(lambda event: self.enterRoom(room="room1")))
        self.btnlogin.config(bg=colors.blue_dark, fg="#FFFFFF",activebackground=colors.blue_light, activeforeground=colors.blue_dark)

        # Submit button
        self.btnlogin = Button(self.window, text='Room2', width=15, bg=colors.blue_dark,fg=colors.blue_dark, command= lambda: self.leaveRoom("room1"))
        self.btnlogin.place(relx=0.5, y=2,anchor=CENTER)

        self.btnlogin.bind('<Return>',(lambda event: self.leaveRoom(room="room1")))
        self.btnlogin.config(bg=colors.blue_dark, fg="#FFFFFF",activebackground=colors.blue_light, activeforeground=colors.blue_dark)

        self.topFrame.pack(side=tk.TOP)

        self.displayFrame = tk.Frame(self.window)
        self.lblLine = tk.Label(
            self.displayFrame, text="*********************************************************************").pack()
        self.scrollBar = tk.Scrollbar(self.displayFrame)
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tkDisplay = tk.Text(self.displayFrame, height=20, width=55)
        self.tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
        self.tkDisplay.tag_config("tag_your_message", foreground="blue")
        self.scrollBar.config(command=self.tkDisplay.yview)
        self.tkDisplay.config(yscrollcommand=self.scrollBar.set,
                              background="#F4F6F7", highlightbackground="grey", state="disabled")
        self.displayFrame.pack(side=tk.TOP)

        self.bottomFrame = tk.Frame(self.window)
        self.tkMessage = tk.Text(self.bottomFrame, height=2, width=55)
        self.tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
        self.tkMessage.config(highlightbackground="grey", state="normal")
        self.tkMessage.bind("<Return>", (lambda event: self.getChatMessage(
            self.tkMessage.get("1.0", tk.END))))
        self.bottomFrame.pack(side=tk.BOTTOM)
        self.window.mainloop()



    def enterRoom(self,room):
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
        # if len(self.entName.get()) < 1:
        #     tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
        # else:
        # self.username = self.entName.get()
        print(self.username)
        self.connect_to_server(self.username)
        # server = SenderRabbitmqConfigure(queue='hello',
        #                    host='localhost',
        #                    routingKey='hello',
        #                    exchange='room1')
        # sender = Sender(server)
        # sender.connect()
        # sender.send_message(msg="hello ya zebi")
        # serverconfigure = ReceiverRabbitMqConfigure(host='localhost',
        #                                   queue='hello',exchange='room1')

        # receiver = Receiver(config=serverconfigure)
        # receiver.connect()
        # receiver.async_consumer(cb=self.print_success)

    def print_success(self, *args):
        print("success")
        print(args)

    def connect_to_server(self, name):
        global client, HOST_PORT, HOST_ADDR
        try:
            # print(self.username)
            # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # client.connect((HOST_ADDR, HOST_PORT))
            # client.send(self.username.encode()) # Send name to server after connecting

            # self.entName.config(state=tk.DISABLED)
            # self.btnConnect.config(state=tk.DISABLED)
            # self.tkMessage.config(state=tk.NORMAL)

            # start a thread to keep receiving message from server
            # do not block the main thread :)
            # threading._start_new_thread(self.receive_message_from_server, (client, "m"))
            # threading._start_new_thread(self.receiver.async_consumer(cb=self.receive_message_from_server), (client, "m"))
            # server = SenderRabbitmqConfigure(queue=self.username,
            #                    host='localhost',
            #                    routingKey='hello',
            #                    exchange='room1')
            # serverconfigure = ReceiverRabbitMqConfigure(host='localhost',
            #                                     queue=self.username,exchange='room1')
            # self.sender = Sender(server)
            # self.sender.connect()
            # self.receiver = Receiver(config=serverconfigure)
            # self.receiver.connect()
            # self.tkMessage.bind("<Return>", (lambda event: self.getChatMessage(self.tkMessage.get("1.0", tk.END))))

            # self.receive_message_from_server, ("client",)
            threading._start_new_thread(
                self.receive_message_from_server, ("client",))
            threading._start_new_thread(
                self.receive_message_from_controller, ("client",))
        except Exception as e:
            print(e)
            tk.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR +
                                    " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")

    def receive_message_from_controller(self, c):
        def callback(ch, method, properties, body):
            print("new connection", body)
            # ch.basic_ack(delivery_tag=method.delivery_tag)
        while True:
            print("in loop")
            self.controller_receiver.listen_channel(callback)

    def receive_message_from_server(self, c):
        self.msg = ''

        def callback(ch, method, properties, body):
            message = ControllerMessageFormat()
            message.convertToJson(body.decode())
            self.handleAction(message.action, message.data)

            print('in', body)
            self.msg = body
            # ch.basic_ack(delivery_tag=method.delivery_tag)
            texts = self.tkDisplay.get("1.0", tk.END).strip()
            self.tkDisplay.config(state=tk.NORMAL)
            if len(texts) < 1:
                self.tkDisplay.insert(tk.END, self.msg.decode())
            else:
                self.tkDisplay.insert(tk.END, "\n\n"+self.msg.decode())

            self.tkDisplay.config(state=tk.DISABLED)
            self.tkDisplay.see(tk.END)

        while True:
            # from_server = sck.recv(4096).decode()
            print('befoooooooooooooooree')
            self.receiver.listen_channel(callback)
            # if not from_server: break

            print('out', self.msg)
            # display message from server on the chat window

            # enable the display area and insert the text and then disable.
            # why? Apparently, tkinter does not allow us insert into a disabled Text widget :(

            # texts = self.tkDisplay.get("1.0", tk.END).strip()
            # self.tkDisplay.config(state=tk.NORMAL)
            # if len(texts) < 1:
            #     self.tkDisplay.insert(tk.END, self.msg)
            # else:
            #     self.tkDisplay.insert(tk.END, "\n\n"+self.msg)

            # self.tkDisplay.config(state=tk.DISABLED)
            # self.tkDisplay.see(tk.END)

            # print("Server says: " +from_server)

        # sck.close()
        # self.window.destroy()

    def handleAction(self,action,data):
        if action == "left":
            user_left=data['user_left']

            texts = self.tkDisplay.get("1.0", tk.END).strip()
            self.tkDisplay.config(state=tk.NORMAL)
            if len(texts) < 1:
                self.tkDisplay.insert(tk.END, user_left.decode())
            else:
                self.tkDisplay.insert(tk.END, "\n\n"+user_left.decode())

            self.tkDisplay.config(state=tk.DISABLED)
            self.tkDisplay.see(tk.END)
        # if action == "connected":
        #     self.connected_users=data["connected_users"]
        #     self.rooms=data['rooms']
        #     #todo later

            
        # elif action == "joined":
        #     self.users_in_room=data['users_in_room']
           

    def getChatMessage(self, msg):

        msg = msg.replace('\n', '')
        texts = self.tkDisplay.get("1.0", tk.END).strip()
        
        self.sender.send_message(msg=msg)
        # enable the display area and insert the text and then disable.
        # why? Apparently, tkinter does not allow use insert into a disabled Text widget :(
        self.tkDisplay.config(state=tk.NORMAL)
        if len(texts) < 1:
            self.tkDisplay.insert(tk.END, "You->" + msg,
                                  "tag_your_message")  # no line
        else:
            self.tkDisplay.insert(
                tk.END, "\n\n" + "You->" + msg, "tag_your_message")

        self.tkDisplay.config(state=tk.DISABLED)

        # self.send_mssage_to_server(msg)

        self.tkDisplay.see(tk.END)
        self.tkMessage.delete('1.0', tk.END)

    def send_mssage_to_server(self, msg):
        client_msg = str(msg)
        client.send(client_msg.encode())
        if msg == "exit":
            client.close()
            self.window.destroy()
        print("Sending message")


# t=ChatInterface()
