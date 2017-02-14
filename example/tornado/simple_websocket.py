import logging
import time
from tornado import websocket
from tornado import ioloop
from tornado import web
import ujson

clients = {}

logger = logging.getLogger(__name__)


class WebsocketHandler(websocket.WebSocketHandler):

    def prepare(self):
        print '>> prepare'

    def check_origin(self, origin):
        print '>> check_origin', origin
        return True

    def open(self):
        print '>> open'
        clients[id(self)] = self

    def call_shutdown(self):
        pass
            

    def on_message(self, message):
        print '>> on_message'
        self.write_message(message)
        if 'shutdown' in message:
            #ioloop.PeriodicCallback(self.call_shutdown, 2000).start()
            self.close()
            

    def on_close(self):
        print '>> on_close'
        del clients[id(self)]
        self.close()

    def close(self):
        print '>> close'
        super(WebsocketHandler, self).close()


if __name__ == '__main__':
	 io_loop = ioloop.IOLoop.instance()
	 app = web.Application(handlers=[
        (r'/ws', WebsocketHandler)
        ])

	 app.listen(9922)
	 io_loop.start()
