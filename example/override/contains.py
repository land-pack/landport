"""
override the `in` operate
"""

class GameRoom(object):
	user_db = []

	def __init__(self, name):
		self.name = name

	def join(self, uid):
		self.user_db.append(uid) 

	def leave(self, uid):
		if uid in self.user_db:
			self.user_db.remove(uid)

	def __contains__(self, item):
		return True if item in self.user_db else False


if __name__ == '__main__':
	gr = GameRoom('fuckroom')
	gr.join('123')
	gr.join('678')
	print('123' in gr)
	print('456' in gr)
	print('678' in gr)
	