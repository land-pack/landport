import logging
import time
from tornado import websocket
from tornado import ioloop
from tornado import web
import ujson
import gevent
from gevent import monkey

monkey.patch_all()

clients = {}

logger = logging.getLogger(__name__)

# def check_in(obj):
#     if obj.arg.get("uid") != '456':
#         obj.write_message("see you later~")
#         gevent.sleep(2)
#         return False
#     return True

class AuthWebSocket(object):

    def __init__(self, obj):
        self.obj = obj

    def check_in(self):
        raise NotImplementedError

    def init_ttl(self):
        raise NotImplementedError

    def init_data(self):
        raise NotImplementedError


    def go(self):
        self.check_in()
        self.init_ttl()
        data = self.init_data()
        if data is None or not isinstance(data, str):
            raise ValueError("init_data() must return a string instead of type(data)=%s" % type(data))
        self.obj.write_message(data)

class MyAuth(AuthWebSocket):
    def check_in(self):
        pass

    def init_ttl(self):
        pass

    def init_data(self):
        return 'something'

class WebsocketHandler(websocket.WebSocketHandler):

    def prepare(self):
        d = {k:v[0] for k, v in self.request.arguments.iteritems()}
        self.arg = d
                
    def check_origin(self, origin):
        return True

    def open(self):
        print '>> open'
        MyAuth(self).go()
        
    def call_shutdown(self):
        pass
            

    def on_message(self, message):
        print '>> on_message'
        self.write_message(message)
        if 'shutdown' in message:
            #ioloop.PeriodicCallback(self.call_shutdown, 2000).start()
            self.close(102, 'shutdown by client command')
            

    def on_close(self):
        print '>> on_close'
        # del clients[id(self)]
        # self.close()

    def close(self, code, reason):
        print '>> close',code, reason
        super(WebsocketHandler, self).close(code, reason)


if __name__ == '__main__':
	 io_loop = ioloop.IOLoop.instance()
	 app = web.Application(handlers=[
        (r'/ws', WebsocketHandler)
        ])

	 app.listen(9922)
	 io_loop.start()
