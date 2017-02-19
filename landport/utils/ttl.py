import time
import traceback
import logging
from tornado import ioloop

logger = logging.getLogger('simple')


class TTLManager(object):
    """
    Set some thing during a time check it whether timeout!
    """

    def __init__(self, timeout=20, ttl_type='ping', frequency=2000, detail=True):
        self._key_hash_time = {}
        self._id_hash_handler = {}
        self.timeout = timeout
        self.ttl_type = ttl_type
        self.frequency = frequency
        self.detail = detail
        self.uid_set = []
        self.seq = {}


    def update(self, key):
        str_key = self.ttl_type + str(id(key))
        self._key_hash_time[str_key] = time.time()
        self._id_hash_handler[str_key] = key
        self.uid_set.append(key.arg.get('uid'))
        self.seq[str_key] = 0

    def is_expire(self, key):
        distance = time.time() - self._key_hash_time[key]
        if distance > self.timeout:
            return 'expire'
        else:
            self.seq[key] += 1
            return distance

    def clean_expire(self):
        del_key = []
        for key in self._key_hash_time:
            distance = self.is_expire(key)
            if self.detail:
                logger.debug("Checker from %s:seq=%suid=%sttl=%stime=%s ms",
                             self.ttl_type,
                             self.seq[key],
                             self._id_hash_handler[key].arg.get('uid'),
                             self.timeout,
                             distance
                             )
            if distance is 'expire':
                handler = self._id_hash_handler[key]
                
                try:
                    handler.close_when_expire(ttl_type=self.ttl_type, code=107, reason='hb timeout')
                except:
                    logger.error(traceback.format_exc())
                else:
                    del_key.append(key)
        for key in del_key:
            self._remove(key)

    def _remove(self, key): 
        if key in self._key_hash_time:
            del self._key_hash_time[key]

        if key in self._id_hash_handler:
            del self._id_hash_handler[key]

        if key in self.seq:
            del self.seq[key]

    def remove(self, handler):
        str_key = self.ttl_type + str(id(handler))
        self._remove(str_key)
        if handler.uid in self.uid_set:
            self.uid_set.remove(handler.arg.get('uid'))

    def start(self):
        ioloop.PeriodicCallback(self.clean_expire, self.frequency).start()
