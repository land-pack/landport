import logging
import logging.config
from websocket import WebsocketHandler
from websocket import AuthWebSocket
from websocket import UserConnectManager
from tornado import ioloop
from tornado import web


logging.config.fileConfig("./etc/dev_log.conf")
logger = logging.getLogger('simple')


class MyAuth(AuthWebSocket):
    def check_in(self):

        if self.obj.arg.get("uid") != '456':
            self.obj.write_message("see you later~")
            # gevent.sleep(2)
            return False
        return True

    def join_room(self):
        uid =self.obj.arg.get("uid")
        room=self.obj.arg.get("room")
        UserConnectManager.join(uid, room, self)
        return True

    def init_ttl(self):
        return True

    def init_data(self):
        return 'something'

class MyWebSocketHandler(WebsocketHandler):
    def open(self):
        print '>> open'
        MyAuth(self).go()
          

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
        super(MyWebSocketHandler, self).close(code, reason)


if __name__ == '__main__':
	 io_loop = ioloop.IOLoop.instance()
	 app = web.Application(handlers=[
        (r'/ws', MyWebSocketHandler)
        ])

	 app.listen(9922)
	 io_loop.start()
