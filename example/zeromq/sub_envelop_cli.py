#!/usr/bin/python
#-*-coding:utf-8-*-

import time
import zmq  
from zmq.eventloop import ioloop
context = zmq.Context()  
socket = context.socket(zmq.SUB)  
socket.connect("tcp://127.0.0.1:6666")  
# socket.setsockopt(zmq.SUBSCRIBE,'xxx') 

loop = ioloop.IOLoop.instance()
def landport(channel):
	def _wrapper(f):
		socket.setsockopt(zmq.SUBSCRIBE, b"{}".format(channel))
		loop.add_handler(socket, f, zmq.POLLIN)
		def __wrapper(*args, **kwargs):
			return f
		return __wrapper
	return _wrapper

@landport("xxx")
def req_handler(sock, events):
	# msg = sock.recv()
	[address, contents] = sock.recv_multipart()
	print("[%s] %s" % (address, contents))
	# print msg

@landport("A")
def req_handler2(sock, events):
	# msg = sock.recv()
	[address, contents] = sock.recv_multipart()
	print("[%s] %s" % (address, contents))

loop.start()