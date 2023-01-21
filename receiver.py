import pika
from threading import Thread


class ReceiverRabbitMqConfigure:
    def __init__(
        self,
        host="localhost",
        queue="",
        exchange="",
        exchange_type="fanout",
        exclusive=True,
    ):

        """Server initialization"""
        self.host = host
        self.queue = queue
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.exclusive = exclusive


class Receiver:
    def __init__(self, config, user=None):
        self.user = user
        self.config = config

    def connect(self):
        self.exchange = self.config.exchange
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config.host)
        )

        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.config.exchange, exchange_type=self.config.exchange_type
        )
        result = self.channel.queue_declare(
            queue=self.config.queue, exclusive=self.config.exclusive
        )

        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.config.exchange, queue=self.queue_name)

    def listen_channel(self, cb):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=cb, auto_ack=True
        )
        self.channel.basic_qos(prefetch_count=0)
        self.channel.start_consuming()

    def async_consumer(self, cb):
        worker = Thread(target=self.listen_channel, args=[cb])
        worker.start()

    def discard_channel(self):
        self.channel.stop_consuming()
