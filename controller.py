import pika
from controller_message_format import ControllerMessageFormat


class Controller:
    def __init__(self):
        self.connected_users = []
        self.rooms = {'room1': [], 'room2': [], 'room3': [], 'room4': []}

    def connectToRabbitmq(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange='from_client_to_controller', exchange_type='direct')
        result = self.channel.queue_declare(queue='main_queue')

        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange='from_client_to_controller', queue=self.queue_name)
        self.receive()

    def receive(self):
        

        def callback(ch, method, properties, body):
            print('############################',body.decode())
            message = ControllerMessageFormat()
            message.convertToJson(body.decode())
            self.handleAction(message.action, message.data)
            # ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(
            queue='main_queue', on_message_callback=callback,auto_ack=True)
        print('Server Started !! Listening')
        self.channel.basic_qos(prefetch_count=0)
        self.channel.start_consuming()

    def send(self,msg,routing_key=''):
        self.channel.exchange_declare(exchange='controller_exchange', exchange_type='fanout')
        self.channel.basic_publish(
            exchange='controller_exchange',
            routing_key=routing_key,
            body=msg,
            # properties=pika.BasicProperties(
            #     delivery_mode=2,  # make message persistent
            # )
            )
    
    def handleAction(self, action, data):
        if action == "onNewConnection":
            # data={username}
            print('============' , data['username'],action)
            self.connected_users.append(data['username'])
            message = ControllerMessageFormat(
                "connected", {"connected_users": self.connected_users, "rooms": self.rooms})
            message.convertToString()
            # self.send(message.msg,routing_key='global_receiver')
            self.send(message.msg)



c=Controller()
c.connectToRabbitmq()
