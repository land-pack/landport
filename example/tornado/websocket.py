from tornado import websocket
from tornado import ioloop
from tornado import web

class WebsocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        pass

    def on_message(self, message):
        self.write_message(message)

    def on_close(self):
        NodeManager.unregister(self)



if __name__ == '__main__':
	 io_loop = ioloop.IOLoop.instance()
	 app = web.Application(handlers=[
        (r'/ws', WebsocketHandler)
        ])

	 app.listen(9922)
	 io_loop.start()