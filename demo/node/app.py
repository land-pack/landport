import logging
import ujson
import traceback
from landport.core.websocket import WebsocketHandler
from landport.core.user import UserConnectManager
from landport.core.auth import AuthWebSocket, DestoryWebSocket
from landport.utils import color
from landport.core.sub import topic
from dispatch import MyCenterMessageDispatcher

logger = logging.getLogger('simple')


@topic("SystemNotify", "GameRealtimeMessage")
def sub_handler(sock, events):
    [address, contents] = sock.recv_multipart()
    logger.info("[%s] %s" % (address, contents))
    try:
        MyCenterMessageDispatcher(contents).go()
    except:
        logger.error(traceback.format_exc())

class MyAuth(AuthWebSocket):

    def join_room(self):
        logger.info('join room')
        uid =self.obj.arg.get("uid")
        room=self.obj.arg.get("room")
        UserConnectManager.join(uid, room, self.obj)
        return True

    def init_ttl(self):
        self.obj.ttl.update(self.obj)
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
                'members':members,
                'numbers':len(members)
            }
        }
        notify_d  = {
            'messageid': '2012',
            'messagetype': 'user_in',
            'body':{
                'info':'I am {}, i in now!'.format(uid)
            }

        }
        logger.info('notify_d=%s', notify_d)
        UserConnectManager.send_other(room, notify_d, uid)
        return ujson.dumps(init_d)


class MyDestory(DestoryWebSocket):
    def check_out(self):
        return True
    
    def asyn_check_out(self):
        return True

    def leave_room(self):
        UserConnectManager.leave(self.obj)
        return True

    def del_ttl(self):
        return True

    def final(self):
        room = self.obj.arg.get('room')
        uid = self.obj.arg.get('uid')     
        notify_d  = {
            'messageid': '2013',
            'messagetype': 'user_out',
            'body':{
                'info':'I am {}, i out now!'.format(uid)
            }
        }
        logger.info('notify_d=%s', notify_d)
        UserConnectManager.send_other(room, notify_d, uid)