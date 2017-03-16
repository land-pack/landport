import ujson

class RanklistBase(dict):
    def __init__(self, name, r, ex=30):
        self.name = name
        self.redis_handler = r
        self.ex = ex
        self.ranklist = []


    def push_in(self, d):
        self._profit(d)
        uid = d.get("uid")
        uid = str(uid)
        d.update({"uid": uid})
        self[uid] = d

    def pop_out(self, data):
        pass

    def __lt__(self, other):
        pass

    def __contains__(self, item):
        pass

    def _profit(self, d):
        p = d.get("prize") - d.get("gold")
        d.update({"profit": p})

    def sort_by(self, key):
        self.ranklist = sorted(self.values(), lambda x, y: cmp(x[key], y[key]), reverse=True)
        return self

    def sort_by_many(self, *args):
        pass

    def add_rank(self, skip_the_same=True):
        j = 1
        new_rank_list = []
        for i in self.ranklist:
            i.update({
                "rank": str(j)
            })
            j += 1
            new_rank_list.append(i)
        self.ranklist = new_rank_list
        return self

    def add_gift(self, gift_config):
        j = 1
        gift_config = self._extend_dict(gift_config)
        new_rank_list = []
        for i in self.ranklist:
            rank_num = i.get("rank")
            i.update({
                "gift": gift_config.get(str(rank_num))
            })
            j += 1
            new_rank_list.append(i)
        self.ranklist = new_rank_list
        return self

    def add_value_from(self, callback, input_field, output_field):
        """
        :param key: the key field name, callback should always return a string value
        :param callback: a string type
        :return: self object
        """
        j = 1
        new_rank_list = []
        for i in self.ranklist:
            input_value = i.get(input_field)
            i.update({
                output_field: callback(input_value)
            })
            j += 1
            new_rank_list.append(i)
        self.ranklist = new_rank_list
        return self

    def add_trend(self, ref_field="rank"):
        the_cache = self.redis_handler.get(self.name) or '{}'
        the_cache = ujson.loads(the_cache)
        for uid, v in self.iteritems():
            if uid in the_cache:
                p = int(v.get(ref_field))
                c = int(the_cache.get(uid).get(ref_field))
                if p < c:
                    v.update({"trend": "1"})
                elif p == c:
                    v.update({"trend": "0"})
                else:
                    v.update({"trend": "-1"})
            else:
                v.update({"trend": "1"})
        new_ranlist = []
        for i in self.ranklist:
            uid = i.get("uid")
            trend = self.get(uid).get("trend")
            i.update({"trend": trend})
            new_ranlist.append((i))
        self.ranklist = new_ranlist
        d = ujson.dumps(self)
        self.redis_handler.set(self.name, d, self.ex)
        return self

    def _extend_dict(self, d):
        """
        Input:
            a = {
                "1":"hello world",
                "2~5":"range between 2~5",
                "6~7":"range between 6~7"
            }
        Output:
            {
                '1': 'helloworld',
                '3': 'rangebetween2~5',
                '2': 'rangebetween2~5',
                '5': 'rangebetween2~5',
                '4': 'rangebetween2~5',
                '7': 'rangebetween6~7',
                '6': 'rangebetween6~7'
            }
        """
        new_d = {}
        for k, v in d.iteritems():
            if '~' in k:
                start, end = k.split('~')
                keys = range(int(start), int(end) + 1)
                for i in keys:
                    new_d.update({
                        str(i): v
                    })
            else:
                new_d.update({
                    k: v
                })
        return new_d

    def rank(self):
        return self.ranklist if self.ranklist else self.values()