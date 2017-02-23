import traceback
import logging
import logging.config
from tornado import ioloop
from tornado import web
from app import WebsocketHandler
from app import MyAuth, MyDestory
from dispatch import MyClientMessageDispatcher
from landport.utils.ttl import TTLManager


logging.config.fileConfig("../etc/dev_log.conf")
logger = logging.getLogger('simple')

ttl_hb = TTLManager(timeout=150, ttl_type='ping', detail=True)
ttl_hb.start()

# ttl_hv = TTLManager(timeout=25, ttl_type='hv', detail=True)
# ttl_hv.start()

class MyWebSocketHandler(WebsocketHandler):
    def open(self):
        self.bind_ttl(ttl_hb)
        #self.bind_ttl(name='hv', ttl_hv)
        MyAuth(self).go()

    def on_message(self, message):
        try:
            MyClientMessageDispatcher(self, message).go()
        except:
            logger.error(traceback.format_exc())

    def on_close(self):
        MyDestory(self).go()

if __name__ == '__main__':
    logger.info("Start server - listen on port: 9922")
    io_loop = ioloop.IOLoop.instance()
    app = web.Application(handlers=[
    (r'/ws', MyWebSocketHandler)
    ])

    app.listen(9922)
    io_loop.start()
