from tornado import ioloop, web, websocket
from tornado.options import options, define
from xpika import PikaClient

define("port", default=9922, type=int, help="run on the given port")

class MyWebSocketHandler(websocket.WebSocketHandler):

    def prepare(self):
        d = {k:v[0] for k, v in self.request.arguments.iteritems()}
        self.arg = d

    def check_origin(self, origin):
        return True


    def open(self):
        print("Open WebSocket")
        roomid = self.arg.get("roomid")
        self.pika_client = PikaClient(roomid=roomid)
        self.pika_client.websocket = self
        io_loop = ioloop.IOLoop.instance()
        # io_loop.add_timeout(1000, self.pika_client.connect)
        self.pika_client.connect()
        self.pika_client.sample_message("someone in ~ with roomid")

    def on_message(self, message):
        print("New Message:{}".format(message))
        self.pika_client.sample_group_message(message)


    def on_close(self):
        print("Closed WebSocket")       
        roomid = self.arg.get("roomid")
        # self.pika_client.sample_message("someone in ~ with roomid={}".format(roomid))
        self.pika_client.connection.close()

if __name__ == '__main__':
    options.parse_command_line()
    port = options.port
    print("Start server - listen on port: {}".format(port))
    io_loop = ioloop.IOLoop.instance()
    app = web.Application(handlers=[
    (r'/ws', MyWebSocketHandler)
    ])
    pc = PikaClient(roomid='something')
    app.pika = pc
    app.listen(port)
    io_loop.start()