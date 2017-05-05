from tornado import ioloop, web, websocket
import ujson
from xpika import PikaClient

class JoinHandler(web.RequestHandler):

    def get(self):
        data = {
            "rtype":"1", # 1:random; 2:custom;
            "rid":"xh72hd24hd39" ,# uuid
            "uid":"98223833"
        }
        self.write(data)



if __name__ == '__main__':
    print("Start server - listen on port: 9933")
    pc = PikaClient(roomid='default')
    io_loop = ioloop.IOLoop.instance()
    io_loop.add_timeout(1000, pc.connect)
    app = web.Application(handlers=[
    (r'/join', JoinHandler)
    ])
    app.listen(9933)
    io_loop.start()