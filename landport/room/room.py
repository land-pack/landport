class Room(object):
    def __init__(self, name, size=9):
        self.unused = 0
        self.size = size
        self.name = name
        self.memebers = set()

    def join(self, uid):
        if uid in self.memebers:
            return self.name
        else:
            self.unused +=1
            self.memebers.add(uid)
            return self.name

    def leave(self, uid):
        if uid in self.memebers:
            self.memebers.remove(uid)
            self.unused-=1
            return True
        else:
            raise ValueError("uid:<%s> no in the room:<%s>" % (uid, self.name))

    def is_empty(self):
        return self.unused == 0

    def is_full(self):
        return self.unused == self.size

    def is_ready_full(self):
        return self.unused == self.size - 1 

    def is_available(self):
        return self.unused < self.size

    def __lt__(self, other):
        return self.unused < other.unused

    def __str__(self):
        return 'room:<%s>' % self.name

    def __repr__(self):
        return self.__str__()


class RoomManager(object):
    uid_to_room = {}
    uid_to_created = {}
    vip_to_room = {}
    room_set = []
    available_room = []
    full_room = []
    empty_room = []

    @classmethod
    def get_room(cls, uid):
        if cls.available_room:
            r = max(cls.available_room)
            if r.is_ready_full(): #if full pick next if_ready_full() size=8
                cls.available_room.remove(r)
        elif cls.empty_room:
            r = max(cls.empty_room)
            cls.available_room.append(r)
            cls.empty_room.remove(r)
        else:
            new_name = NodeManager.gen_room_name() or '{:6f}'.format(time.time())
            r = Room(new_name)
            cls.available_room.append(r)
        r.join(uid)
        return r

    @classmethod
    def get_room_name(cls, uid):
        if uid in cls.uid_to_room:
            return cls.uid_to_room[uid]
        else:
            #TODO book stratge ...
            room = cls.get_room(uid)
            cls.uid_to_room[uid] = room
            if room.is_full():
                cls.full_room.append(room)
            return room.name

    @classmethod
    def book(cls, uid):
        room_name = cls.get_room_name(uid)
        create_time = time.time()
        created = '{:6f}'.format(create_time)
        cls.uid_to_created[uid]=created 
        #ip, port = room_name.split('-')
        data = {
            # 'ip':ip,
            # 'port':port,
            # 'node':ip-port,
            'room': room_name,
            'created': created,
            'uid':uid
        }
        #TODO cls.set_ttl(uid, create_time, expire=5)
        return data

    @classmethod
    def vip_book(cls, uid):
        pass


    @classmethod
    def cancel(cls, uid):
        if uid in cls.uid_to_room:
            room = cls.uid_to_room[uid]
            room.leave(uid)
            if room.is_empty():
                cls.available_room.remove(room)
                cls.empty_room.append(room)
            if room in cls.full_room:
                cls.full_room.remove(room)
                cls.available_room.append(room)
            del cls.uid_to_room[uid]
            del cls.uid_to_created[uid]
        else:
            raise ValueError('No uid=%s on the room' % (uid))


    @classmethod
    def check_in(cls, uid, create_time):
        if cls.uid_to_created.get(uid, None) == create_time:
            return True
        else:
            return False


    @classmethod
    def check_out(self, uid, create_time):
        if cls.uid_to_created.get(uid, None) == create_time:
            cls.cancel(uid)
        else:
            raise ValueError("No uid=%s check in", uid)




if __name__ == '__main__':
    # r1 = Room('a')
    # print r1.join('123')
    # print r1.join('1234')
    # r2 = Room('b')
    # print r2.join('123')
    # print r2.join('1234')
    # print r2.join('1222')
    # print r2.join('1224')
    # r3 = Room('c')
    # print r3.join('123')
    # print r3.join('1234')
    # print r3.join('1222')
    # print r3.join('1224')
    # print r3.join('12246')
    # r = [r1, r2, r3]
    # print max(r)
    # print min(r)
    # r3.leave('123')
    # r3.leave('1234')
    # r = [r1, r2, r3]
    # print max(r)
    # print min(r)
    # print r3.is_available()
    # print r3.is_empty()
    # print r3.is_full()
    # already_book = []
    # for i in range(100):
    #     time.sleep(0.5)
    #     RoomManager.book('0100{}'.format(i))
    #     already_book.append(i)
    #     if len(already_book) > 20:
    #         for i in already_book:
    #             print '*'*30
    #             if i % 2==0:
    #                 RoomManager.cancel('0100{}'.format(i))
    #         already_book = []
    #     print RoomManager.available_room
    #     print RoomManager.uid_to_room
    # print RoomManager.book('1234123')
    # print RoomManager.available_room
    # print RoomManager.uid_to_room
    # try:
    #     RoomManager.cancel('1234123')
    # except Exception as ex:
    #     print (str(ex))
    # print RoomManager.available_room
    # print RoomManager.uid_to_room
    for i in range(10):
        RoomManager.book(i)
    print RoomManager.available_room
    print RoomManager.full_room
    RoomManager.cancel(2)
    print RoomManager.available_room
    print RoomManager.full_room

