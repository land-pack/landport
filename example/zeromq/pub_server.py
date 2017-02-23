import zmq
from zmq.eventloop import ioloop

loop = ioloop.IOLoop.instance()

ctx = zmq.Context()
s1 = ctx.socket(zmq.REP)
s1.bind('tcp://127.0.0.1:5555')

s2 = ctx.socket(zmq.PUB)
s2.bind('tcp://127.0.0.1:6666')

def rep_handler(sock, events):
    # We don't know how many recv's we can do?
    msg = sock.recv()
    # No guarantee that we can do the send. We need a way of putting the
    # send in the event loop.
    sock.send(msg)
    s2.send_string('xxx hello thisisbrodcast')

 # socket = context.socket(zmq.SUB)  
 # socket.connect("tcp://127.0.0.1:5050")  
 # socket.setsockopt(zmq.SUBSCRIBE,'') 
# def pub_handler(sock, events):
# 	msg = sock.recv()
# 	sock.send('this is publise message')

loop.add_handler(s1, rep_handler, zmq.POLLIN)
# loop.add_handler(s2, pub_handler, zmq.POLLIN)
loop.start()