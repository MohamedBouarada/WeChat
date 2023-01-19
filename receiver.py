import pika
from threading import Thread

class ReceiverRabbitMqConfigure():

    def __init__(self, host='localhost', queue='hello',exchange=''):

        """ Server initialization   """
        self.host = host
        self.queue = queue
        self.exchange=exchange

class Receiver():
    def __init__(self,config, user=None):
        self.user = user
        self.config=config

    def connect(self):
        self.exchange = self.config.exchange
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config.host))

        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.config.exchange, exchange_type='fanout')
        result = self.channel.queue_declare(queue='', exclusive=True)

        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.config.exchange, queue=self.queue_name)
        print('ready to receive msg')

    def listen_channel(self, cb):
        print('listeeen   nayek')
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=cb, auto_ack=True)
        print('call')
        self.channel.basic_qos(prefetch_count=0)
        self.channel.start_consuming()
        print("shutdown broker!")

    def async_consumer(self, cb):
        worker = Thread(target=self.listen_channel, args=[cb])
        worker.start()

    def discard_channel(self):
        self.channel.stop_consuming()
        # self.connection.close()

# def callb(ch,method,properties,body):
#     print('received ',body)

# serverconfigure = ReceiverRabbitMqConfigure(host='localhost',
#                                                queue='',exchange='room1')   
# r=Receiver(serverconfigure)
# r.connect()
# r.listen_channel(callb)