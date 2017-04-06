class Base():
	__slots__ = []

	def __setattr__(self, key, name):
		if not key in self.__slots__:
			raise AttributeError("Can set attrubute name as:{}".format(key))

class MyClass(Base):
	pass