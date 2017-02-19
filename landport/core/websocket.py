import logging
import time
from tornado import websocket
from tornado import ioloop
from tornado import web
import ujson
import gevent
from gevent import monkey


CHECK_IN_FAILURE = 101
JOIN_ROOM_FAILURE = 102
INIT_TTL_FAILURE  = 103
CHECK_OUT_FAILURE = 104
DEL_TTL_FAILURE = 105
LEAVE_ROOM_FAILURE = 106


monkey.patch_all()

clients = {}

logger = logging.getLogger('simple')


class AuthWebSocket(object):

    def __init__(self, obj):
        self.obj = obj

    def check_in(self):
        """
        Here you can sync data to your roomserver!
        """
        raise NotImplementedError

    def join_room(self):
        """
        Register the new user to your local UserConnectManager!
        """
        raise NotImplementedError

    def init_ttl(self):
        """
        Set ttl for the new connect handler!
        """
        raise NotImplementedError

    def init_data(self):
        """
        Here you can fetch user information from your database!
        """
        raise NotImplementedError


    def go(self):
        if not self.check_in():self.obj.close(CHECK_IN_FAILURE, 'check_in_failure')
        if not self.init_ttl():self.obj.close(INIT_TTL_FAILURE, 'init_ttl_failure')
        if not self.join_room():self.obj.close(JOIN_ROOM_FAILURE, 'join_room_failure')
        data = self.init_data()
        if data is None or not isinstance(data, str):
            raise ValueError("init_data() must return a string instead of type(data)=%s" % type(data))
        self.obj.write_message(data)

class DestoryWebSocket(object):
    def __init__(self, obj):
        self.obj = obj

    def check_out(self):
        """
        Send check out request to roomserver by `HTTP`
        """
        return True
    
    def asyn_check_out(self):
        """
        Send check out request to roomserver by `WEBSOCKET`
        """
        return True

    def leave_room(self):
        raise NotImplementedError

    def del_ttl(self):
        raise NotImplementedError

    def final(self):
        raise NotImplementedError

    def go(self):
        if not self.check_out():self.obj.close(CHECK_OUT_FAILURE, 'check_out_failure')
        if not self.asyn_check_out():self.obj.close(CHECK_OUT_FAILURE, 'check_out_failure')
        if not self.del_ttl():self.obj.close(DEL_TTL_FAILURE, 'del_ttl_failure')
        if not self.leave_room():self.obj.close(LEAVE_ROOM_FAILURE, 'leave_room_failure')
        self.final()

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
