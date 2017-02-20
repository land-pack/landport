import logging
import time
from tornado import websocket
from tornado import ioloop
from tornado import web
import ujson


clients = {}

logger = logging.getLogger('simple')




class WebsocketHandler(websocket.WebSocketHandler):

    def prepare(self):
        d = {k:v[0] for k, v in self.request.arguments.iteritems()}
        self.arg = d
        logger.info('websocket arguments:%s', d)
                
    def check_origin(self, origin):
        return True

    def bind_ttl(self, ttl):
        setattr(self, 'ttl', ttl)

    def close_when_expire(self, ttl_type, code, reason):
        logger.debug("Clean bad websock handler:\tuid=%s", self.arg.get('uid'))
        if ttl_type == 'ping':
            logger.warning("Heart beat expire:\tid(connect)=%s\tuid=%s", id(self), self.arg.get('uid'))
            self.close(code, reason)
    #     try:
    #         # kick_off_uid.append(id(self))
    #         # self.send_kick_off()
    #         # for each in range(5, HEART_BEAT_TIMEOUT, 5):
    #         #     ioloop.IOLoop.instance().add_timeout(time.time() + each, self.send_kick_off)
    #         # ioloop.IOLoop.instance().add_timeout(time.time() + HEART_BEAT_TIMEOUT + 2, self.remove_heart_beat)
    #         # ioloop.IOLoop.instance().add_timeout(time.time() + HEART_BEAT_TIMEOUT + 5, self.close)
    #         logger.info('notify the user, he has expire ~~')
    #     except Exception as ex:
    #         logger.error(traceback.format_exc())

    def write_message(self, msg):
        logger.info('send msg=%s', msg)
        if not self.stream.closed():
            super(WebsocketHandler, self).write_message(msg)
        else:
            logger.warning("self=%s connect has shutdown", self)

    def close(self, code, reason):
        logger.warning('>>close:code=%s|reason=%s',code, reason)
        super(WebsocketHandler, self).close()
