from tornado import ioloop, web, websocket
from xpika import PikaClient

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
        io_loop.add_timeout(1000, self.pika_client.connect)

    def on_message(self, message):
        print("New Message:{}".format(message))
        self.pika_client.sample_group_message(message)


    def on_close(self):
        print("Closed WebSocket")
        self.pika_client.connection.close()

if __name__ == '__main__':
    print("Start server - listen on port: 9922")
    io_loop = ioloop.IOLoop.instance()
    app = web.Application(handlers=[
    (r'/ws', MyWebSocketHandler)
    ])
    pc = PikaClient(roomid='something')
    app.pika = pc
    app.listen(9922)
    io_loop.start()