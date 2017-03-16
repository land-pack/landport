#!coding: utf-8
class BaseModel(object):
	def __init__(self, how='r'):
		self.how = how
		if 'r' == self.how:
			self.conn = db_pool.get_mysql("crazy_bet_r")
		else:
			self.conn = db_pool.get_mysql("crazy_bet")
		self.cursor = self.conn.cursor(MySQLdb.cursor.DictCursor)
			
	def __del__(self):
		if self.conn: self.conn.close()


class ExampleModel(BaseModel):

	def login(self, uid):
		pass

# p = ExampleModel('r').login(uid=1234)
#优点：在每个调用处指明调用的数据库访问类型，调用端明确
#缺点：修改点较多~~工作量大
#
#====================================
class DB():
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return '%s' % self.name

	def __repr__(self):
		self.__str__()

	def cursor(self):
		pass

	def close(self):
		print 'close ...'


class BaseModel(object):
	def __init__(self):
		# self.conn_rw = db_pool.get_mysql("crazy_bet_r") or '123'
		# self.cursor_rw = self.conn.cursor(MySQLdb.cursor.DictCursor) or '456'
		# self.conn_r = db_pool.get_mysql("crazy_bet") or '789'
		# self.cursor_r = self.conn.cursor(MySQLdb.cursor.DictCursor) or '110'
		# self.cursor = None
		self.conn_rw = DB('rw')
		self.conn_w = DB('w')
		self.conn_r = DB('r')
		self.conn = None
		self.cursor ='dict cursor'
		
	def __del__(self):
		if self.conn_r: self.conn_r.close()
		if self.conn_rw: self.conn_rw.close()

def access(level, cursor='dict'):
	def _wrapper(f):
		def __wrapper(*args, **kwargs):
			obj = args[0]
			params = args[1:]

			if level == 'r':
				setattr(obj, 'conn', getattr(obj,'conn_r'))
			elif level == 'w':
				setattr(obj, 'conn', getattr(obj,'conn_w'))
			else:
				setattr(obj, 'conn', getattr(obj,'conn_rw'))
			if cursor == 'list':
				setattr(obj, 'cursor', obj.conn.cursor() or 'list ..')
			return f(*args, **kwargs)
		return __wrapper
	return _wrapper



class ExampleModel(BaseModel):

	@access('r')
	def login(self, uid, name):
		print 'hello connection=%s--uid=%s--name=%s' % (self.conn, uid, name)

	@access('w')
	def logout(self, uid, name):
		print 'hello connection=%s--uid=%s--name=%s' % (self.conn, uid, name)

	@access('rw')
	def register(self, uid, name):
		print self.cursor
		print 'hello connection=%s--uid=%s--name=%s' % (self.conn, uid, name)

	@access('rw', cursor='list')
	def unregister(self, uid, name):
		print 'self.cursor', self.cursor
		print 'hello connection=%s--uid=%s--name=%s' % (self.conn, uid, name)


if __name__ == '__main__':
	ExampleModel().login('123', 'name')
	ExampleModel().logout('123', name='name')
	ExampleModel().register(uid='123', name='name')
	ExampleModel().unregister('123', 'fran')


