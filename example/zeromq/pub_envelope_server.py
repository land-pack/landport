"""

   Pubsub envelope publisher

   Author: Guillaume Aubert (gaubert) <guillaume(dot)aubert(at)gmail(dot)com>

"""
import time
import zmq
import ujson

a = {
    "messagetype":"hello",
    "messageid":"10003",
    "body":{
        "good":"fine"
    }
}

b = {
    "messagetype":"hey",
    "messageid":"10004",
    "body":{
        "good":"fine"
    }
}

def main():
    """main method"""

    # Prepare our context and publisher
    context   = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:6666")

    while True:
        # Write two messages, each with an envelope and content
        publisher.send_multipart([b"SystemNotify", ujson.dumps(a)]) #hello
        publisher.send_multipart([b"GameRealtimeMessage", ujson.dumps(b)]) #hey
        time.sleep(1)

    # We never get here but clean up anyhow
    publisher.close()
    context.term()

if __name__ == "__main__":
    main()