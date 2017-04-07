#!/usr/bin/python
#-*-coding:utf-8-*-

import zmq
import sys
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
port = 5555
socket.bind("tcp://*:%s" % port)

while True:
    #  Wait for next request from client
    message = socket.recv()
    print "Received request: ", message
    socket.send(message)
    time.sleep (1)

