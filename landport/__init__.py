import logging
import logging.config
from websocket import WebsocketHandler
from websocket import AuthWebSocket
from websocket import UserConnectManager
from tornado import ioloop
from tornado import web
import ujson

logging.config.fileConfig("./etc/dev_log.conf")
logger = logging.getLogger('simple')


class MyAuth(AuthWebSocket):
    def check_in(self):

        # if self.obj.arg.get("uid") != '456':
        #     self.obj.write_message("see you later~")
        #     # gevent.sleep(2)
        #     return False
        return True

    def join_room(self):
        uid =self.obj.arg.get("uid")
        room=self.obj.arg.get("room")
        UserConnectManager.join(uid, room, self.obj)
        return True

    def init_ttl(self):
        return True

    def init_data(self):
        room = self.obj.arg.get('room')
        uid = self.obj.arg.get('uid')
        members = UserConnectManager.members(room)
        logger.info(members)
        #fetch they information by name
        #let other members know i in~
        init_d = {
            'messageid':'2000',
            'messagetype':'init',
            'body':{
                'members':[
                    'frank',
                    'jack',
                    'lisa'
                ],
                'numbers':'3'
            }
        }
        notify_d  = {
            'messageid': '2012',
            'messagetype': 'user_in',
            'body':{
                'info':'I am 123, i in now!'
            }

        }
        # UserConnectManager.send(self.obj, init_d)
        logger.info('notify_d=%s', notify_d)
        UserConnectManager.send_other(room, notify_d, uid)
        return ujson.dumps(init_d)

class MyWebSocketHandler(WebsocketHandler):
    def open(self):
        logger.info('>> open')
        MyAuth(self).go()
          

    def on_message(self, message):
        print '>> on_message'
        self.write_message(message)
        if 'shutdown' in message:
            #ioloop.PeriodicCallback(self.call_shutdown, 2000).start()
            self.close(102, 'shutdown by client command')
            

    def on_close(self):
        logger.info('>> on_close')
        room = self.arg.get('room')
        uid = self.arg.get('uid')

        UserConnectManager.leave(self)
        notify_d  = {
            'messageid': '2013',
            'messagetype': 'user_out',
            'body':{
                'info':'I am 123, i in now!'
            }

        }
        logger.info('notify_d=%s', notify_d)
        UserConnectManager.send_other(room, notify_d, uid)
        # del clients[id(self)]
        # self.close()

if __name__ == '__main__':
    logger.info("Start server - listen on port: 9922")
    io_loop = ioloop.IOLoop.instance()
    app = web.Application(handlers=[
    (r'/ws', MyWebSocketHandler)
    ])

    app.listen(9922)
    io_loop.start()
