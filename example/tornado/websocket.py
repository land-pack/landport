import logging
import time
from tornado import websocket
from tornado import ioloop
from tornado import web
import ujson

clients = {}
kick_off_candidate = []

logger = logging.getLogger(__name__)
HEART_BEAT_TYPE = 'heart_beat_type'
HEART_BEAT_TIMEOUT = 120
heart_beat_ttl_manager = None
operate_ttl_manager = None


class WebsocketHandler(websocket.WebSocketHandler):

    def prepare(self):
        print '>> prepare'

    def check_origin(self, origin):
        print '>> check_origin', origin
        return True

    def open(self):
        print '>> open'
        clients[id(self)] = self

    def on_message(self, message):
        print '>> on_message'
        self.write_message(message)
        try:
            msg = ujson.loads(message)
        except Exception as ex:
            if "p" in msg:
                self.write_message("q")
                heart_beat_ttl_manager.update(self)
            else:
                logger.error("Unknow message structure")
        else:
            WSRoute.route(self, msg)


    def on_close(self):
        print '>> on_close'
        del clients[id(self)]
        if self.is_handler_has_updated():
            logger.info('remove [%s] from kick_off_candiate', self.uid)
        else:
            try:
                heart_beat_ttl_manager.remove(self)
            except Exception as ex:
                logger.error(ex)

            try:
                operate_ttl_manager.remove(self)
            except Exception as ex:
                logger.error(ex)

            try:
                WSRoute.deluser(self)
            except Exception as ex:
                logger.error(ex)



    def close(self):
        print '>> close'
        super(WebsocketHandler, self).close()

class HandlerManager(WebsocketHandler):

    def kick_off(self):
        id_handler = id(self)
        if id_handler in clients:
            clients[id_handler].close()

    def clean_handler(self, clean_type):
        if clean_type == HEART_BEAT_TYPE:
            try:
                self.close()
            except Exception as ex:
                logger.error(ex)
        else:
            kick_off_candidate.append(self.uid)
            start_time = time.time()
            for i in range(5, HEART_BEAT_TIMEOUT, 5):
                ioloop.IOLoop.instance().add_timeout(start_time + i, self.send_kick_off_message)
            ioloop.IOLoop.instance().add_timeout(start_time + HEART_BEAT_TIMEOUT + 2, self.remove_ttl)
            ioloop.IOLoop.instance().add_timeout(start_time + HEART_BEAT_TIMEOUT + 5, self.close)  

    def send_kick_off_message(self):
        msg = {
            "messagetype":"kick_off",
            "messageid": "2016",
            "body": {}
        }
        try:
            self.write_message(ujson.dumps(msg))
        except Exception as ex:
            logger.error(ex)


    def remove_ttl(self):
        if self.uid in kick_off_candidate:
            kick_off_candidate.remove(self.uid)
        heart_beat_ttl_manager.remove(self)

    def is_handler_has_updated(self):
        if self.uid in heart_beat_ttl_manager.uid_set and uid in kick_off_candidate:
            kick_off_candidate.remove(self.uid)
            
            return True
        else:
            return False



if __name__ == '__main__':
	 io_loop = ioloop.IOLoop.instance()
	 app = web.Application(handlers=[
        (r'/ws', WebsocketHandler)
        ])

	 app.listen(9922)
	 io_loop.start()