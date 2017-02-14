import logging
import traceback

from concurrent import futures

thread_executor = futures.ThreadPoolExecutor(max_workers=50)
logger = logging.getLogger(__name__)

class WebSocketConnectManager(object):
	uid_to_handler = {}
	room_to_uid = {}

	@classmethod
	def register(cls, handler):
		pass

	@classmethod
	def unregister(cls, handler):
		pass

	@classmethod
	def route(cls, handler, req):
		pass

	@classmethod
	def send(cls, handler, rsp):
		try:
			thread_executor.submit(handler.write_message, rsp)
		except:
			logger.error(traceback.format_exc())

	@classmethod
	def send_by_room(cls, handler, rsp):
		pass

	@classmethod
	def send_to_everyone(cls, handler, rsp):
		uid_to_handler = copy.copy(cls.uid_to_handler)
		for uid, handler in uid_to_handler.iteritems():
			cls.send(handler,rsp=rsp)







