#!/usr/bin/python
#-*-coding:utf-8-*-

import zmq
import sys

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

while(True):
    data = raw_input("input your data:")
    if data == 'q':
        sys.exit()

    socket.send(data)

    response = socket.recv();
    print response