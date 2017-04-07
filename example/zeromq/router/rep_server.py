import zmq

context = zmq.Context()

socket = context.socket(zmq.REP)
socket.connect("tcp://127.0.0.1:5560")

while True:
	m = socket.recv()
	print('work for>>>%s' % m)
	m+='Server A'
	socket.send(m)
