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
def landport(*channel):
	def _wrapper(f):
		for i in channel:
			socket.setsockopt(zmq.SUBSCRIBE, b"{}".format(i))
			loop.add_handler(socket, f, zmq.POLLIN)
		def __wrapper(*args, **kwargs):
			return f
		return __wrapper
	return _wrapper

# @landport("SystemNotify")
@landport("GameRealtimeMessage","SystemNotify")
def req_handler(sock, events):
	# msg = sock.recv()
	[address, contents] = sock.recv_multipart()
	print("?xxx [%s] %s" % (address, contents))
	# print msg

# @landport("GameRealtimeMessage")
def req_handler2(sock, events):
	# msg = sock.recv()
	[address, contents] = sock.recv_multipart()
	print("XXXAAA [%s] %s" % (address, contents))

# socket.setsockopt(zmq.SUBSCRIBE, b"{}".format('GameRealtimeMessage'))
# loop.add_handler(socket, req_handler, zmq.POLLIN)
# socket.setsockopt(zmq.SUBSCRIBE, b"{}".format('SystemNotify'))
# loop.add_handler(socket, req_handler2, zmq.POLLIN)
loop.start()