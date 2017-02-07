from tornado import websocket
from tornado import ioloop
from tornado import web

clients = {}



class WebsocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        print '>> check_origin'
        return True

    def open(self):
        print '>> open'
        clients[id(self)] = self

    def on_message(self, message):
        print '>> on_message'
        self.write_message(message)
        if 'shutdown' in message:
            io_loop = ioloop.IOLoop.instance()
            ioloop.PeriodicCallback(self.kick_off, 5000).start()
            self.write_message('shutdown handler after 5s')

    def on_close(self):
        print '>> on_close'
        del clients[id(self)]

    def close(self):
        print '>> close'
        super(WebsocketHandler, self).close()

    def kick_off(self):
        id_handler = id(self)
        if id_handler in clients:
            clients[id_handler].close()


if __name__ == '__main__':
	 io_loop = ioloop.IOLoop.instance()
	 app = web.Application(handlers=[
        (r'/ws', WebsocketHandler)
        ])

	 app.listen(9922)
	 io_loop.start()