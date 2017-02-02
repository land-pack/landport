import zmq
import time
context = zmq.Context()
 
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://127.0.0.1:5556")
subscriber.connect("tcp://127.0.0.1:5557")
subscriber.setsockopt(zmq.SUBSCRIBE, "")
 
publisher = context.socket(zmq.PUB)
# publisher.bind("ipc://nasdaq-feed")
publisher.bind("tcp://127.0.0.1:7777")
 
while True:
    message = subscriber.recv()
    print 'recv:{}'.format(message)
    publisher.send(message)
    