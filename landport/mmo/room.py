class RM(set):

    def __init__(self, name, size=5):
        self.name = name
        self.size = size
        self.available = 0


class RManager(dict):

    def join(self, req):
        """
        Example req:
        {
            "type": "1"  # 1 -> random / 2 -> new / 3 ->
            "uid": "12345"
        }
        """
        req_type = req.get("type")
        req_uid = req.get("uid")
        if req_uid in self:
        	return self.get(req_uid)

        if req_type == "3":
            return _join_with_invitation(uid)
        elif req_type == "2":
            return _join_with_new(uid)
        else:
            return _join_with_random(uid)

    def _join_with_random(self, uid):
        """
        Fill a room with priority
        """
        if self.has_available_room()
        uuid = 'UUID by node'
        room = Room(name=uuid)



    def _join_with_new(self, uid):
        pass

    def _join_with_invitation(self, uid, code):
        pass


if __name__ == '__main__':
    rm = RM('sample')
    rm.add(123)
    rm.add(897)
    print 'rm status', rm
