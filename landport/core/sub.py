#!/usr/bin/python
#-*-coding:utf-8-*-

import time
import zmq  
from zmq.eventloop import ioloop
context = zmq.Context()  
socket = context.socket(zmq.SUB)  
socket.connect("tcp://127.0.0.1:6666")  
loop = ioloop.IOLoop.instance()

def topic(*channel):
	def _wrapper(f):
		for i in channel:
			socket.setsockopt(zmq.SUBSCRIBE, b"{}".format(i))
			loop.add_handler(socket, f, zmq.POLLIN)
		def __wrapper(*args, **kwargs):
			return f
		return __wrapper
	return _wrapper