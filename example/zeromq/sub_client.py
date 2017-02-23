#!/usr/bin/python
#-*-coding:utf-8-*-

import time
import zmq  
from zmq.eventloop import ioloop
context = zmq.Context()  
socket = context.socket(zmq.SUB)  
socket.connect("tcp://127.0.0.1:6666")  
socket.setsockopt(zmq.SUBSCRIBE,'xxx') 

loop = ioloop.IOLoop.instance()
# while True:  
#     print  socket.recv()

# def rep_handler(sock, events):
#     # We don't know how many recv's we can do?
#     msg = sock.recv()
#     print 'sub message', msg

# loop.add_handler(socket, rep_handler, zmq.POLLIN)
def landport(channel):
	def _wrapper(f):
		socket.setsockopt(zmq.SUBSCRIBE, channel)
		loop.add_handler(socket, f, zmq.POLLIN)
		def __wrapper(*args, **kwargs):
			return f
		return __wrapper
	return _wrapper

@landport("xxx")
def req_handler(sock, events):
	msg = sock.recv()
	print msg

loop.start()