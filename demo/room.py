from landport.room.node import NodeManager
from landport.room.room import RoomManager
from tornado.web import RequestHandler
from landport.core.sub import topic
from landport.core.dispatch import CenterDispatchManager


class JoinHandler(RequestHandler):
	def get(self):
		pass

class MyNodeManager(NodeManager):
	def __init__(self):
		pass

"""
client.sub("self-ip+self-port")
def process_
"""

class MyDispatch(CenterDispatchManager):
	def node_connect(self, data):
		ip = data.get("ip")
		port = data.get("port")
		MyNodeManager.add_node(ip, port)

	def user_check_in(self, data):
		pass

	def user_check_out(self, data):
		pass

	def node_disconnect(self, data):
		pass

@topic("RoomSubNode")
def room_sub(sock, events):
	[address, contents] = sock.recv_multipart()
	MyDispatch(contents).go()


if __name__ == '__main__':
    logger.info("Start room server - listen on port: 9921")
    io_loop = ioloop.IOLoop.instance()
    app = web.Application(handlers=[
    (r'/join', JoinHandler)
    ])

    app.listen(9921)
    io_loop.start()