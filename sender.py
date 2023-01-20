import pika

class SenderRabbitmqConfigure():

    def __init__(self, queue='', host='localhost', routingKey='', exchange='',exchange_type='fanout'):
        """ Configure Rabbit Mq Server  """
        self.queue = queue
        self.host = host
        self.routingKey = routingKey
        self.exchange = exchange
        self.exchange_type=exchange_type

class Sender():
    def __init__(self,config , user=None):
        self.user = user
        self.config=config

    def connect(self):
        self.exchange = self.config.exchange
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config.host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.config.exchange, exchange_type=self.config.exchange_type)

    def send_message(self, msg='echo'):
        self.channel.basic_publish(
            exchange=self.config.exchange, routing_key=self.config.routingKey, body=msg)
        print(" [x] Sent %r" % msg)

    def disconnect(self):
        self.connection.close()

# server = SenderRabbitmqConfigure(queue='',
#                                host='localhost',
#                                routingKey='hello',
#                                exchange='room1')
# s=Sender(server)
# s.connect()
# s.send_message(msg='ya3tek 3asba')