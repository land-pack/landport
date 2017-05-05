import uuid
import collections
import bisect


class VirtualRoom(object):

	# __slots__ == ['']
	members = []
	members_info = {}

	def __init__(self, name, size):
		self.name = name
		self.size = size


	@classmethod
	def join(cls, uid):
		if uid in cls.members:
			return cls.members_info[uid]


	@classmethod
	def leave(self, uid):
		pass


if __name__ == '__main__':
	roomid = VirtualRoom.join('12345')

