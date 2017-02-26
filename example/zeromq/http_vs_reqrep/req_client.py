import zmq
import sys
import time

port = "9944"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

context = zmq.Context()
print "Connecting to server..."
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
if len(sys.argv) > 2:
    socket.connect ("tcp://localhost:%s" % port1)

#  Do 10 requests, waiting each time for a response
start = time.time()
for request in range (100000):
    # print "Sending request ", request,"..."
    socket.send ("123|456")
    #  Get the reply.
    message = socket.recv()
    # print "Received reply ", request, "[", message, "]"

end = time.time()

print 'time cost:%6f' % (end - start)