from tornado import websocket
from tornado import ioloop
from tornado import web




class JoinHandler(web.RequestHandler):
    def get(self):
        num1 = self.get_argument("num1")
        num2 = self.get_argument("num2")
        self.write('%s' % (int(num2)+int(num1)))



if __name__ == '__main__':
	app = web.Application(handlers=[
		(r'/', JoinHandler)
		])
	io_loop = ioloop.current().instance()
	app.listen(9933)
	io_loop.start()
