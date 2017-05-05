class MyAttrClass(type):
	def __new__(cls, clsname, bases, dct):
		my_attr = {}
		for name, value in dct.items():
			if not name.startswith("__"):
				my_attr["my_" + name] = value
			else:
				my_attr[name] = value 
		return type.__new__(cls, clsname, bases, my_attr)

class Foo():
	__metaclass__ = MyAttrClass
	test_age = 1
	test_name = "test"

print(hasattr(Foo, "test_age"))
print(hasattr(Foo, "my_test_age"))