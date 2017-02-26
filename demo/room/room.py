import ujson
# from landport.room.room import Room
import logging
import logging.config
import zmq
from tornado import web
from zmq.eventloop import ioloop
loop = ioloop.IOLoop.instance()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % 9321)

logging.config.fileConfig("../etc/room_log.conf")
logger = logging.getLogger('simple')

class JoinHandler(web.RequestHandler):
    def get(self):
        num1 = self.get_argument("num1")
        num2 = self.get_argument("num2")
        self.write('%s' % (int(num2)+int(num1)))


def f(sock, events):
	message = sock.recv()
	data = ujson.loads(message)
	uid = data.get('uid')
	created = data.get('created')
	logger.info('uid=%s--created=%s', uid, created)
	ok = True
	if ok:
		sock.send('yes')
	else:
		sock.send('no')


if __name__ == '__main__':
    logger.info("Start room server - listen on port: 9933")
    app = web.Application(handlers=[
    	(r'/join', JoinHandler)
    ])
    loop.add_handler(socket, f, zmq.POLLIN)
    app.listen(9933)
    loop.start()