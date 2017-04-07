import logging
import traceback
import ujson
from concurrent import futures


MAX_THREADS = 100
thread_executor = futures.ThreadPoolExecutor(max_workers=MAX_THREADS)
logger = logging.getLogger('simple')


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
            thread_executor.submit(handler.write_message, ujson.dumps(msg))
        except:
            logger.error(traceback.format_exc())

    @classmethod
    def send_other(cls, room, msg, sender):
        logger.info('send message to other except uid=%s', sender)
        for uid in cls.room_2_uid_set[room] or []:
            if uid == sender: continue
            handler = cls.uid_2_handler.get(uid)
            cls.send(handler, msg)

    @classmethod
    def send_all(cls, room, msg):
        logger.info("Send all user with msg=%s", msg)
        cls.send_other(room, msg, sender=None)

    @classmethod
    def broadcast(cls, msg):
        for room in cls.room_2_uid_set:
            cls.send_all(room, msg)