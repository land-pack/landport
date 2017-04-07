import time
import ujson


class NodeInformation(object):

    def __init__(self, handler, rooms=0):
        self.ip = handler.ip
        self.port = handler.port
        self.node_id = "{}-{}".format(self.ip, self.port)
        self.rooms = rooms
        self.room_set = set()
        self.origin_node_id = handler.node
        setattr(handler, 'node', self.node_id)
        setattr(handler, 'ni', self)

class NodeManager(object):
    nodeid_hash_nodeinfo = {}
    max_rooms = 50

    @classmethod
    def register(cls, handler):
        node_info = NodeInformation(handler)
        cls.nodeid_hash_nodeinfo[node_info.node_id] = node_info
        if node_info.origin_node_id == "-1":
            return ujson.dumps({'method': 'connect', 'node': node_info.node_id})
        else:
            return ujson.dumps({'method': 'recovery'})

    @classmethod
    def unregister(cls, handler):
        release_rooms = handler.ni.room_set
        del cls.nodeid_hash_nodeinfo[handler.ni.node_id]
        return release_rooms

    @classmethod
    def gen_room_name(cls):
        for node_id, node_info in cls.nodeid_hash_nodeinfo.iteritems():
            if node_info.rooms < cls.max_rooms:
                node_info.rooms += 1
                room_name = '{}-{:6f}'.format(node_info.node_id,time.time())
                node_info.room_set.add(room_name)
                return room_name
        return None


