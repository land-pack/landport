import logging
import time
from tornado import websocket
from tornado import ioloop
from tornado import web
import ujson
import gevent
from gevent import monkey
from concurrent import futures
from utils import color
MAX_THREADS = 100
thread_executor = futures.ThreadPoolExecutor(max_workers=MAX_THREADS)
CHECK_IN_FAILURE = 101
JOIN_ROOM_FAILURE = 102
INIT_TTL_FAILURE  = 103

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


class WebsocketHandler(websocket.WebSocketHandler):

    def prepare(self):
        d = {k:v[0] for k, v in self.request.arguments.iteritems()}
        self.arg = d
        logger.info('websocket arguments:%s', d)
                
    def check_origin(self, origin):
        return True

    def close_when_expire(self, code, reason):
        pass

    def write_message(self, msg):
        if not self.stream.closed():
            super(WebsocketHandler, self).write_message(msg)
        else:
            logger.warning("self=%s connect has shutdown", self)

    def close(self, code, reason):
        logger.warning('>>close:code=%s|reason=%s',code, reason)
        super(WebSocketHandler, self).close(code, reason)


class UserConnectManager(object):

    room_2_uid_set = {}
    uid_2_handler = {}

    @classmethod
    def clean_old_handler(cls, handler):
        handler.close()

    @classmethod
    def join(cls, uid, room, handler):

        if uid in cls.uid_2_handler:
            cls.clean_old_handler(cls.uid_2_handler[uid])
        cls.uid_2_handler[uid] = handler

        if room in cls.room_2_uid_set:
            cls.room_2_uid_set[room].add(uid)
        else:
            cls.room_2_uid_set[room] = set([uid,])

        logger.info("uid=%s join successfully", uid)

    @classmethod
    def members(cls, room):
        return cls.room_2_uid_set[room]

    @classmethod
    def leave(cls, handler):
        uid = handler.arg.get('uid')
        if uid in cls.uid_2_handler:
            del cls.uid_2_handler[uid]

        room = handler.arg.get("room")
        if uid in cls.room_2_uid_set[room]:
            cls.room_2_uid_set[room].remove(uid)
            
    @classmethod
    def send(cls, handler, msg):
        try:
            # logger.info("send to receiver uid=%s\tmsg=%s", handler.uid, msg)
            thread_executor.submit(handler.write_message, ujson.dumps(msg))
        except:
            logger.error(traceback.format_exc())

    @classmethod
    def send_other(cls, room, msg, sender):
        logger.info('send message to other except uid=%s', sender)
        for uid in cls.room_2_uid_set[room] or []:
            if uid == sender: continue
            handler = cls.uid_2_handler.get(uid)
            logger.info('handler is %s', handler)
            cls.send(handler, msg)

    @classmethod
    def send_all(cls, room, msg):
        cls.send_other(cls, room, msg, sender=None)

    @classmethod
    def broadcast(cls, msg):
        for room in cls.room_2_uid_set:
            cls.send_all(room, msg)


if __name__ == '__main__':
	 io_loop = ioloop.IOLoop.instance()
	 app = web.Application(handlers=[
        (r'/ws', MyWebSocketHandler)
        ])

	 app.listen(9922)
	 io_loop.start()
