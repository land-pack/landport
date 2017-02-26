import zmq
import ujson

CHECK_IN_FAILURE = 101
JOIN_ROOM_FAILURE = 102
INIT_TTL_FAILURE  = 103
CHECK_OUT_FAILURE = 104
DEL_TTL_FAILURE = 105
LEAVE_ROOM_FAILURE = 106
port = 9321

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)


class AuthWebSocket(object):

    def __init__(self, obj):
        """
        Set Websocket handler as `obj` attribute!
        """
        self.obj = obj

    def check_in(self):
        """
        Here you can sync data to your roomserver!
        Usage:
            1. Ask your roomserver, is the guy valid
            2. When the guy register on the roomserver
            the local node will also receiver some notify
            from the roomserver by WebSocket, so when the guy
            connect to the local node, will directory check in!
            3. ...
        """
        uid = self.obj.arg.get("uid")
        created = self.obj.arg.get("created")
        data = {
            "uid":uid,
            "created":created
        }
        socket.send(ujson.dumps(data))
        #  Get the reply.
        message = socket.recv()
        if message == 'yes':
            return True
        else:
            return False

    def join_room(self):
        """
        Register the new user to your local UserConnectManager!
        """
        raise NotImplementedError

    def init_ttl(self):
        """
        Set ttl for the new connect handler!
        """
        raise NotImplementedError

    def init_data(self):
        """
        Here you can fetch user information from your database!
        """
        raise NotImplementedError


    def go(self):
        if not self.check_in():self.obj.close(CHECK_IN_FAILURE, 'check_in_failure')
        if not self.init_ttl():self.obj.close(INIT_TTL_FAILURE, 'init_ttl_failure')
        if not self.join_room():self.obj.close(JOIN_ROOM_FAILURE, 'join_room_failure')
        data = self.init_data()
        if data is None or not isinstance(data, str):
            raise ValueError("init_data() must return a string instead of type(data)=%s" % type(data))
        self.obj.write_message(data)

class DestoryWebSocket(object):
    def __init__(self, obj):
        self.obj = obj

    def check_out(self):
        """
        Send check out request to roomserver by `HTTP`
        """
        return True
    
    def asyn_check_out(self):
        """
        Send check out request to roomserver by `WEBSOCKET`
        """
        return True

    def leave_room(self):
        raise NotImplementedError

    def del_ttl(self):
        raise NotImplementedError

    def final(self):
        raise NotImplementedError

    def go(self):
        if not self.check_out():self.obj.close(CHECK_OUT_FAILURE, 'check_out_failure')
        if not self.asyn_check_out():self.obj.close(CHECK_OUT_FAILURE, 'check_out_failure')
        if not self.del_ttl():self.obj.close(DEL_TTL_FAILURE, 'del_ttl_failure')
        if not self.leave_room():self.obj.close(LEAVE_ROOM_FAILURE, 'leave_room_failure')
        self.final()