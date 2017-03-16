import sys
import time
import zmq

context = zmq.Context()

# Socket to reiceive message on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

#socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

#process tasks forever
while True:
	s = receiver.recv()

	#simple progress indicator for views
	sys.stdout.write('.')
	sys.stdout.flush()

	#Do the work
	time.sleep(int(s)*0.001)

	#send result to sink
	sender.send('')