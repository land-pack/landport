import time
import zmq

context = zmq.Context()

publisher = context.socket(zmq.PUB)
publisher.bind("tcp://127.0.0.1:5557")
# publisher.setsockopt(zmq.SUBSCRIBE, "NASDAQ")


for i in range(10000):
	publisher.send("Hello,{}".format(i))
	time.sleep(1)