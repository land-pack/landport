import tornado
import pika
from pika.adapters.tornado_connection import TornadoConnection

class PikaClient(object):

    def __init__(self, roomid=None):

        # Construct a queue name we'll use for this instance only

        #Giving unique queue for each consumer under a channel.
        print("init PickClient!")
        self.queue_name = "queue-%s" % (id(self),)
        # Default values
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None

        #Webscoket object.
        self.websocket = None
        self.roomid = roomid

    def connect(self):

        if self.connecting:
                print('PikaClient: Already connecting to RabbitMQ')
                return

        print('PikaClient: Connecting to RabbitMQ on localhost:5672, Object: %s' % (self,))

        self.connecting = True

        # credentials = pika.PlainCredentials('guest', 'guest')
        # param = pika.ConnectionParameters(host='localhost',
        #                                   port=5672,
        #                                   virtual_host="/"
        #                                   credentials=credentials
        #                                   )
        param = pika.ConnectionParameters("localhost")
        self.connection = TornadoConnection(param,
                                            on_open_callback=self.on_connected)

        #Currently this will close tornado ioloop.
        #self.connection.add_on_close_callback(self.on_closed)

    def on_connected(self, connection):
        print('PikaClient: Connected to RabbitMQ on localhost:5672')
        self.connected = True
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):

        print('PikaClient: Channel Open, Declaring Exchange, Channel ID: %s' %
              (channel,))
        self.channel = channel

        self.channel.exchange_declare(exchange='tornado',
                                      type="direct", # fanout > direct > topics > header
                                      auto_delete=True,
                                      durable=False,
                                      callback=self.on_exchange_declared)

    def on_exchange_declared(self, frame):
        print('PikaClient: Exchange Declared, Declaring Queue')
        self.channel.queue_declare(auto_delete=True,
                                   queue=self.queue_name,
                                   durable=False,
                                   exclusive=True,
                                   callback=self.on_queue_declared)

    def on_queue_declared(self, frame):

        print('PikaClient: Queue Declared, Binding Queue')
        self.channel.queue_bind(exchange='tornado',
                                queue=self.queue_name,
                                routing_key='tornado.*',
                                callback=self.on_queue_bound)
        self.channel.queue_bind(exchange='tornado',
                                queue=self.queue_name,
                                routing_key='group.{}'.format(self.roomid),
                                callback=self.on_queue_bound)

    def on_queue_bound(self, frame):
        print('PikaClient: Queue Bound, Issuing Basic Consume')
        self.channel.basic_consume(consumer_callback=self.on_pika_message,
                                   queue=self.queue_name,
                                   no_ack=True)

    def on_pika_message(self, channel, method, header, body):
        print('PikaCient: Message receive, delivery tag #%i' %
              method.delivery_tag)

        #Send the Cosumed message via Websocket to browser.
        self.websocket.write_message(body)

    def on_basic_cancel(self, frame):
        print('PikaClient: Basic Cancel Ok')
        # If we don't have any more consumer processes running close
        self.connection.close()

    def on_closed(self, connection):
        # We've closed our pika connection so stop the demo
        tornado.ioloop.IOLoop.instance().stop()

    def sample_message(self, ws_msg):
        #Publish the message from Websocket to RabbitMQ
        properties = pika.BasicProperties(
            content_type="text/plain", delivery_mode=1)

        self.channel.basic_publish(exchange='tornado',
                                   routing_key='tornado.*',
                                   body=ws_msg,
                                   properties=properties)

    def sample_group_message(self, ws_msg):
        #Publish the message from Websocket to RabbitMQ
        properties = pika.BasicProperties(
            content_type="text/plain", delivery_mode=1)

        self.channel.basic_publish(exchange='tornado',
                                   routing_key='group.{}'.format(self.roomid),
                                   body=ws_msg,
                                   properties=properties)
