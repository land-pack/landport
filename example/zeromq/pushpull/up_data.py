import zmq
import random

context = zmq.Context()

#socket to send message on
sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5557")

print("Press Enter when the worker are ready:")
_ = raw_input()

print("Sending tasks to workers ...")

# The first message is "0" and signals start of batch
sender.send('0')

random.seed()

# send 100 tasks

total_mesc = 0
for task_nbr in range(100):
	#Random worload from 1 to 100 msec
	worload = random.randint(1, 100)
	total_mesc += worload
	sender.send(str(worload))
print("Total expected cost:%s msec" % total_mesc)