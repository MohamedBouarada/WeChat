import pika
from controller_message_format import ControllerMessageFormat


class Controller:
    def __init__(self):
        self.connected_users = []
        self.rooms = {"room1": [], "room2": [], "room3": [], "room4": []}

    def connectToRabbitmq(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange="from_client_to_controller", exchange_type="direct"
        )
        result = self.channel.queue_declare(queue="main_queue")

        self.queue_name = result.method.queue
        self.channel.queue_bind(
            exchange="from_client_to_controller", queue=self.queue_name
        )
        self.receive()

    def receive(self):
        def callback(ch, method, properties, body):
            message = ControllerMessageFormat()
            message.convertToJson(body.decode())
            self.handleAction(message.action, message.data)
            # ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(
            queue="main_queue", on_message_callback=callback, auto_ack=True
        )
        print("Server Started !! Listening")
        self.channel.basic_qos(prefetch_count=0)
        self.channel.start_consuming()

    def send(self, msg, routing_key="", exchange="controller_exchange"):
        self.channel.exchange_declare(exchange=exchange, exchange_type="fanout")
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=msg,
        )

    def handleAction(self, action, data):
        if action == "onNewConnection":
            # data={username}
            self.connected_users.append(data["username"])
            message = ControllerMessageFormat(
                "connected",
                {"connected_users": self.connected_users, "rooms": self.rooms},
            )
            message.convertToString()
            self.send(message.msg)

        elif action == "onRoomEnter":
            # data={username,room}
            self.rooms[data["room"]].append(data["username"])
            message = ControllerMessageFormat(
                "joined",
                {
                    "users_in_room": self.rooms[data["room"]],
                    "current": data["username"],
                    "num_room" : data['room']
                },
            )
            message.convertToString()
            self.send(msg=message.msg)

        elif action == "onRoomLeave":
            # data={username,room}
            self.rooms[data["room"]].remove(data["username"])
            message = ControllerMessageFormat(
                "left",
                {
                    "users_in_room": self.rooms[data["room"]],
                    "user_left": data["username"],
                },
            )
            message.convertToString()
            self.send(msg=message.msg, exchange=data["room"])

        elif action == "onQuit":
            self.connected_users.remove(data["username"])
            message = ControllerMessageFormat(
                "quitted", {"connected_users": self.connected_users}
            )
            message.convertToString()
            self.send(message.msg)
        elif action == "OnGoBackToWelcome":
            message = ControllerMessageFormat(
                "wentBack",
                {"connected_users": self.connected_users, "rooms": self.rooms},
            )
            message.convertToString()
            self.send(message.msg)
        


c = Controller()
c.connectToRabbitmq()
