import tkinter as tk
from tkinter import *

import colors
from tkinter import Button, Frame
import threading
from controller_message_format import ControllerMessageFormat
from receiver import Receiver, ReceiverRabbitMqConfigure

from sender import Sender, SenderRabbitmqConfigure
from rsa_handler import rsa_decrypt, rsa_encrypt
import base64

# network client
client = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080


class ChatInterface(Frame):
    def __init__(
        self, master=None, username="", num_room="", users_in_room=[], wlc=None ,which_room=''
    ):

        self.window = Toplevel()
        self.wlc = wlc
        self.username = username
        self.which_room=which_room
        self.num_room = num_room

        self.connected_users = []
        self.rooms = {"room1": [], "room2": [], "room3": [], "room4": []}
        if(self.which_room == self.num_room):

            self.users_in_room = users_in_room

        server = SenderRabbitmqConfigure(
            queue="hello", host="localhost", routingKey="hello", exchange=self.num_room
        )
        serverconfigure = ReceiverRabbitMqConfigure(
            host="localhost", queue="", exchange=self.num_room
        )
        self.sender = Sender(server)
        self.sender.connect()
        self.receiver = Receiver(config=serverconfigure)
        self.receiver.connect()

        controller_receiver_config = ReceiverRabbitMqConfigure(
            host="localhost",
            queue="",
            exchange="controller_exchange",
            exchange_type="fanout",
            exclusive=False,
        )
        self.controller_receiver = Receiver(controller_receiver_config)
        self.controller_receiver.connect()

        controller_sender_config = SenderRabbitmqConfigure(
            queue="main_queue",
            host="localhost",
            routingKey="main_queue",
            exchange="from_client_to_controller",
            exchange_type="direct",
        )
        self.controller_sender = Sender(controller_sender_config)
        self.controller_sender.connect()
        

        self.connect()

        self.window.geometry("800x500")
        self.window.title("WeChat")
        self.window.config(background=colors.blue_dark)

        self.leftFrame = tk.Frame(self.window, background="white")
        self.listTitle = Label(
            self.leftFrame, text="Chat List", font=("times new roman", 20)
        )
        self.listTitle.config(fg="white", bg=colors.success_bg, width=15)
        self.listTitle.pack()
        self.liste = Listbox(
            self.leftFrame, width=25, height=22, bg="white", fg=colors.blue_1
        )
        self.liste.delete(0, END)
        for user in self.users_in_room:
            self.liste.insert(END, user)

        self.liste.pack()

        self.leaveBtn = Button(
            self.leftFrame,
            text="Leave Room",
            width=10,
            font=("bold", 15),
            bg=colors.blue_dark,
            fg=colors.blue_dark,
            command=lambda: self.leaveRoom(),
        )
        self.leaveBtn.pack(padx=(1, 1), pady=(1, 1))

        self.leaveBtn.bind("<Return>", (lambda event: self.leaveRoom()))
        self.leaveBtn.config(
            bg=colors.blue_dark,
            fg="#FFFFFF",
            activebackground=colors.blue_light,
            activeforeground=colors.blue_dark,
        )

        self.leftFrame.pack(side=tk.LEFT, padx=(20, 20), pady=(20, 20))

        self.displayFrame = tk.Frame(self.window, bg=colors.blue_3, width=400)
        self.lblLine = tk.Label(
            self.displayFrame,
            text=self.num_room,
            bg=colors.blue_3,
            fg=colors.blue_dark,
            font=("times new roman", 22),
        ).pack()

        self.scrollBar = tk.Scrollbar(
            self.displayFrame, bg=colors.blue_2, activebackground=colors.blue_1
        )
        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tkDisplay = tk.Text(
            self.displayFrame, height=21, width=55, bg=colors.blue_3
        )
        self.tkDisplay.pack(side=tk.TOP, fill=tk.Y, padx=(5, 13))
        self.tkDisplay.tag_config("tag_your_message", foreground=colors.blue_1)
        self.tkDisplay.tag_config("on_user_left", foreground=colors.red)
        self.scrollBar.config(command=self.tkDisplay.yview)
        self.tkDisplay.config(
            yscrollcommand=self.scrollBar.set,
            background="white",
            highlightbackground=colors.blue_light,
            state="disabled",
        )

        self.bottomFrame = tk.Frame(self.displayFrame, bg=colors.blue_3)
        self.tkMessage = tk.Text(self.bottomFrame, height=2, width=55)
        self.tkMessage.pack(side=tk.BOTTOM, padx=(5, 13), pady=(5, 10))
        self.tkMessage.config(
            highlightbackground="grey", state="normal", fg=colors.blue_dark
        )
        self.tkMessage.bind(
            "<Return>",
            (lambda event: self.getChatMessage(self.tkMessage.get("1.0", tk.END))),
        )
        self.bottomFrame.pack(side=tk.BOTTOM)

        self.displayFrame.pack(side=tk.LEFT)

        self.window.resizable(0, 0)
        self.window.mainloop()

    def leaveRoom(self):
        message = ControllerMessageFormat(
            "onRoomLeave", {"username": self.username, "room": self.num_room}
        )

        message.convertToString()
        self.controller_sender.send_message(message.msg)
        # self.window.withdraw()
        self.welcome()

    def connect(self):
        global client
        self.connect_to_server(self.username)

    def connect_to_server(self, name):
        global client, HOST_PORT, HOST_ADDR
        try:
            threading._start_new_thread(self.receive_message_from_server, ("client",))
            threading._start_new_thread(
                self.receive_message_from_controller, ("client",)
            )
        except Exception as e:
            print(e)
            tk.messagebox.showerror(
                title="ERROR!!!",
                message="Cannot connect to host: "
                + HOST_ADDR
                + " on port: "
                + str(HOST_PORT)
                + " Server may be Unavailable. Try again later",
            )

    def receive_message_from_controller(self, c):
        def callback(ch, method, properties, body):
            message = ControllerMessageFormat()
            message.convertToJson(body.decode())

            if message.action == "joined":
                if(message.data['num_room']==self.num_room):
                    self.users_in_room = message.data["users_in_room"]
                    self.liste.delete(0, END)
                    for user in self.users_in_room:
                        self.liste.insert(END, user)

        while True:
            self.controller_receiver.listen_channel(callback)

    def receive_message_from_server(self, c):
        self.msg = ""

        def callback(ch, method, properties, body):
            message = ControllerMessageFormat()
            message.convertToJson(body.decode())
            self.handleAction(message.action, message.data)

        while True:
            self.receiver.listen_channel(callback)

    def handleAction(self, action, data):
        if action == "left":
            user_left = data["user_left"]

            self.users_in_room = data["users_in_room"]
            self.liste.delete(0, END)
            for user in self.users_in_room:
                self.liste.insert(END, user)

            texts = self.tkDisplay.get("1.0", tk.END).strip()
            self.tkDisplay.config(state=tk.NORMAL)
            if len(texts) < 1:
                self.tkDisplay.insert(
                    tk.END, user_left + " left the room", "on_user_left"
                )

            else:
                self.tkDisplay.insert(
                    tk.END, "\n\n" + user_left + " left the room", "on_user_left"
                )
            self.tkDisplay.config(state=tk.DISABLED)
            self.tkDisplay.see(tk.END)

        elif action == "onMessageSend":
            msgArray = data["data"]

            encrypted_msg = ""
            for element in msgArray:
                if element["username"] == self.username:
                    encrypted_msg = element["message"]
                    break

            if len(encrypted_msg) > 0:
                decrypted_msg = rsa_decrypt(
                    encrypted_message=encrypted_msg, receiver_username=self.username
                )
                texts = self.tkDisplay.get("1.0", tk.END).strip()
                self.tkDisplay.config(state=tk.NORMAL)
                if len(texts) < 1:
                    self.tkDisplay.insert(
                        tk.END, data["sender"] + "-> " + decrypted_msg.decode()
                    )
                else:
                    self.tkDisplay.insert(
                        tk.END, "\n\n" + data["sender"] + "-> " + decrypted_msg.decode()
                    )

                self.tkDisplay.config(state=tk.DISABLED)
                self.tkDisplay.see(tk.END)

    def getChatMessage(self, msg):

        msg = msg.replace("\n", "")
        texts = self.tkDisplay.get("1.0", tk.END).strip()
        data = []
        for user in self.users_in_room:
            if user != self.username:
                encrypted = rsa_encrypt(message=msg, receiver_username=user)
                decodedMsg = base64.b64decode(encrypted)
                decodedMsg = encrypted.decode("utf-8", "strict")

                data.append({"username": user, "message": decodedMsg})
        message = ControllerMessageFormat(
            action="onMessageSend", data={"data": data, "sender": self.username}
        )
        message.convertToString()

        self.sender.send_message(msg=message.msg)
        self.tkDisplay.config(state=tk.NORMAL)
        if len(texts) < 1:
            self.tkDisplay.insert(tk.END, "You->" + msg, "tag_your_message")  # no line
        else:
            self.tkDisplay.insert(tk.END, "\n\n" + "You->" + msg, "tag_your_message")

        self.tkDisplay.config(state=tk.DISABLED)

        self.tkDisplay.see(tk.END)
        self.tkMessage.delete("1.0", tk.END)

    def send_mssage_to_server(self, msg):
        client_msg = str(msg)
        client.send(client_msg.encode())
        if msg == "exit":
            client.close()
            self.window.destroy()

    def welcome(self):
        self.window.withdraw()
        from welcome import Welcome

        w = Welcome(username=self.username, fromChat="true")


# t=ChatInterface()
