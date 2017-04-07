from tornado import websocket
from tornado import ioloop
from tornado import web
from zmq.eventloop import ioloop
#zeromq
import zmq
import time
import sys


loop = ioloop.IOLoop.instance()

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % 9944)

#
# socket.bind("tcp://*:%s" % port)

# while True:
#     #  Wait for next request from client
#     message = socket.recv()
#     print "Received request: ", message
#     time.sleep (1)
#     socket.send("World from %s" % port)

def f(sock, events):
	message = sock.recv()
	num1, num2 = message.split('|')
	num3 = int(num1) + int(num2)
	sock.send('%s' % num3)


class JoinHandler(web.RequestHandler):
    def get(self):
        num1 = self.get_argument("num1")
        num2 = self.get_argument("num2")
        self.write('%s' % (int(num2)+int(num1)))



if __name__ == '__main__':
	app = web.Application(handlers=[
		(r'/', JoinHandler)
		])
	# io_loop = ioloop.IOLoop.current().instance()
	loop.add_handler(socket, f, zmq.POLLIN)
	app.listen(9933)
	loop.start()
