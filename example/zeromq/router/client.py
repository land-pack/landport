import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)

socket.connect("tcp://127.0.0.1:5559")

while True:
    m = raw_input("Please input message:")
    if m == 'q':
        break

    socket.send(m)
    print socket.recv_multipart()


