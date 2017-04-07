from zmq.eventloop import ioloop
from room import RoomManager

loop = ioloop.IOLoop.instance()

def f(sock, events):
	message = sock.recv()
	data = ujson.loads(message)
	# TODO dispatch message if message more than 3 ~~
	# check_in/check_out
	uid = data.get('uid')
	created = data.get('created')
	#logger.info('uid=%s--created=%s', uid, created)
	status = RoomManager.check_in(uid, created)
	if status:
		sock.send('yes')
	else:
		sock.send('no')



loop.add_handler(socket, f, zmq.POLLIN)