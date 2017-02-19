import traceback
import logging
import logging.config
from tornado import ioloop
from tornado import web
from app import WebsocketHandler
from app import MyAuth, MyDestory
from landport.core.ttl import TTLManager


logging.config.fileConfig("../etc/dev_log.conf")
logger = logging.getLogger('simple')

ttl_hb = TTLManager(timeout=5, ttl_type='ping', detail=False)
ttl_hb.start()


class MyWebSocketHandler(WebsocketHandler):
    def open(self):
        logger.info('>> open')
        self.bind_ttl(ttl_hb)
        # try:
        MyAuth(self).go()
        logger.info('open...')

    def on_message(self, message):
        print '>> on_message'
        self.write_message(message)
        if 'shutdown' in message:
            #ioloop.PeriodicCallback(self.call_shutdown, 2000).start()
            self.close(102, 'shutdown by client command')
            

    def on_close(self):
        logger.info('>> on_close')
        MyDestory(self).go()

if __name__ == '__main__':
    logger.info("Start server - listen on port: 9922")
    io_loop = ioloop.IOLoop.instance()
    app = web.Application(handlers=[
    (r'/ws', MyWebSocketHandler)
    ])

    app.listen(9922)
    io_loop.start()
