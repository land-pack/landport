import sys
import time
import zmq

context = zmq.Context()

receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:5558")

s = receiver.recv()


tstart = time.time()

total_msec = 0

for task_nbr in range(100):
	s = receiver.recv()
	if task_nbr % 10 == 0:
		sys.stdout.write(':')
	else:
		sys.stdout.write('.')

tend = time.time()
print("Total elapsed time: %d msec" % ((tend - tstart)* 1000))