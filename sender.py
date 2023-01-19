import pika

class SenderRabbitmqConfigure():

    def __init__(self, queue='hello', host='localhost', routingKey='hello', exchange=''):
        """ Configure Rabbit Mq Server  """
        self.queue = queue
        self.host = host
        self.routingKey = routingKey
        self.exchange = exchange

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
            exchange=self.config.exchange, exchange_type='fanout')

    def send_message(self, msg='echo'):
        self.channel.basic_publish(
            exchange=self.config.exchange, routing_key='', body=msg)
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