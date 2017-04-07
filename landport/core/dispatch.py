import ujson

class ClientDispatchManager(object):
	def __init__(self, handler, message):
		self.handler = handler
		self.message = message

	def default(self, handler, message):
		self.handler.write_message('unknow messagetype')

	def go(self):
		try:
			data = ujson.loads(self.message)
		except ValueError:
			if 'p' in self.message:
				self.handler.ttl.update(self.handler)
			else:
				self.handler.write_message('echo:{}'.format(self.message))
		else:
			messagetype = data.get('messagetype')
			if messagetype.startswith('_'):
				raise ValueError("Invalid messagetype name {}".format(messagetype))
			getattr(self, messagetype, getattr(self, 'default'))(self.handler, data)


class CenterDispatchManager(object):
	def __init__(self, message):
		self.message = message

	def default(self, message):
		raise ValueError('unknow messagetype: %s' % message)

	def go(self):
		data = ujson.loads(self.message)
		messagetype = data.get('messagetype')
		if messagetype.startswith('_'):
			raise ValueError("Invalid messagetype name {}".format(messagetype))
		getattr(self, messagetype, getattr(self, 'default'))(data)