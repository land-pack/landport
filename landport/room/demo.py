import unittest

class GameRoom(dict):
	def join(self, uid):
		pass

	def check_in(self, uid, created):
		pass

	def check_out(self, uid, created):
		pass

	def leave(self, uid):
		pass







class TestRoom(unittest.TestCase):
	def setUp(self):
		self.gr = GameRoom()

	def test_1_join(self):
		self.gr.join('123')

	def tearDown(self):
		pass