import unittest
import redis
import time
import random

from landport.core.rank import RanklistBase as Ranklist


# your data / maybe from mysql/redis/mongodb, but here we use python dict
# instead!
user_info_data = {
    "1002922": "frank",
    "1002923": "jack",
    "1002924": "pig"
}
rank_prize_data = {
    "1": {"name": "iPhone"},
    "2~3": {"name": "iPod"}
}

# your plugin function declare here ...


def add_profit(d):
    p = d.get("prize") - d.get("gold")
    d.update({"profit": p})


def add_userinfotmation(d):
    uid = d.get("uid")
    username = user_info_data.get(uid)
    d.update({"username": username})


class TestRanklistBase(unittest.TestCase):

    def setUp(self):
        self.redis_connect = redis.Redis("127.0.0.1", 6379, 0)

    def test_1_ranklist_push_in(self):
        rk = Ranklist('last_ranklist_cache', self.redis_connect)
        user_1 = {
            "gold": 120,
            "prize": 220,
            "uid": 1002922
        }
        rk.push_in(user_1)
        expect_result = [{
            "gold": 120,
            "prize": 220,
            "uid": "1002922"
        }, ]
        self.assertEqual(rk.top(), expect_result)

        expect_result = {
            "1002922": {
                "gold": 120,
                "prize": 220,
                "uid": "1002922"
            }
        }
        self.assertEqual(rk, expect_result)

    def test_2_ranklist_plugin(self):
        rk = Ranklist('last_ranklist_cache', self.redis_connect)
        rk.plugin(add_profit)
        rk.plugin(add_userinfotmation)

        user_1 = {
            "gold": 120,
            "prize": 220,
            "uid": 1002922
        }

        rk.push_in(user_1)

        expect_result = [{
            "gold": 120,
            "prize": 220,
            "uid": "1002922",
            "username": "frank",
            "profit": 100,
        }, ]
        self.assertEqual(rk.top(), expect_result)

        expect_result = {
            "1002922": {
                "gold": 120,
                "prize": 220,
                "uid": "1002922",
                "username": "frank",
                "profit": 100,
            }
        }
        self.assertEqual(rk, expect_result)

    def test_3_ranklist_add_rank(self):
        rk = Ranklist('last_ranklist_cache', self.redis_connect)
        rk.plugin(add_profit)
        rk.plugin(add_userinfotmation)

        user_1 = {
            "gold": 120,
            "prize": 220,
            "uid": 1002922
        }

        rk.push_in(user_1)
        rk.sort_by("profit").add_rank()

        expect_result = [{
            "gold": 120,
            "prize": 220,
            "uid": "1002922",
            "username": "frank",
            "profit": 100,
            "rank": "1",
        }, ]
        self.assertEqual(rk.top(), expect_result)

        expect_result = {
            "1002922": {
                "gold": 120,
                "prize": 220,
                "uid": "1002922",
                "username": "frank",
                "profit": 100,
                "rank": "1",
            }
        }
        self.assertEqual(rk, expect_result)

    def test_4_ranklist_add_gift(self):
        rk = Ranklist('last_ranklist_cache', self.redis_connect)
        rk.plugin(add_profit)
        rk.plugin(add_userinfotmation)

        user_1 = {
            "gold": 120,
            "prize": 220,
            "uid": 1002922
        }
        user_2 = {
            "gold": 220,
            "prize": 520,
            "uid": 1002923
        }
        user_3 = {
            "gold": 120,
            "prize": 320,
            "uid": 1002924
        }

        rk.push_in(user_1)
        rk.push_in(user_2)
        rk.push_in(user_3)
        rk.sort_by("profit").add_rank().add_gift(rank_prize_data)

        expect_result = [
            {'username': 'jack',
             'prize': 520,
             'gold': 220,
             'profit': 300,
             'gift': {'name': 'iPhone'},
             'rank': '1',
             'uid': '1002923'
             },
            {'username': 'pig',
             'prize': 320,
             'gold': 120,
             'profit': 200,
             'gift': {'name': 'iPod'},
             'rank': '2',
             'uid': '1002924'
             }
        ]
        self.assertEqual(rk.top(2), expect_result)

    def test_5_ranklist_add_trend(self):
        redis_key = 'last_ranklist_cache:{}'.format(random.randint(1, 1000))
        rk = Ranklist(redis_key, self.redis_connect)
        rk.plugin(add_profit)

        user_1 = {
            "gold": 120,
            "prize": 220,
            "uid": 1002922
        }

        user_2 = {
            "gold": 120,
            "prize": 320,
            "uid": 1002924
        }
        rk.push_in(user_1)
        rk.push_in(user_2)

        expect_result = [
            {'trend': '1',
             'prize': 320,
             'gold': 120,
             'profit': 200,
             'rank': '1',
             'uid': '1002924'
             },
            {'trend': '1',
             'prize': 220,
             'gold': 120,
             'profit': 100,
             'rank': '2',
             'uid': '1002922'
             }
        ]
        rk.sort_by("profit").add_rank().add_trend()
        self.assertEqual(rk.top(), expect_result)
        # after a while ...
        time.sleep(2)
        user_1 = {
            "gold": 220,
            "prize": 620,
            "uid": 1002922
        }
        user_2 = {
            "gold": 120,
            "prize": 320,
            "uid": 1002924
        }

        # simulator come in again ...
        print('redis key ={}'.format(redis_key))
        rk2 = Ranklist(redis_key, self.redis_connect)
        rk2.plugin(add_profit)
        rk2.push_in(user_1)
        rk2.push_in(user_2)
        expect_result = [
            {'trend': '1',
             'prize': 620,
             'gold': 220,
             'profit': 400,
             'rank': '1',
             'uid': '1002922'
             },
            {'trend': '-1',
             'prize': 320,
             'gold': 120,
             'profit': 200,
             'rank': '2',
             'uid': '1002924'
             }

        ]
        rk2.sort_by("profit").add_rank().add_trend()
        self.assertEqual(rk2.top(), expect_result)

    def test_6_plugin_install(self):
        rk = Ranklist('last_ranklist_cache', self.redis_connect)
        user_1 = {
            "gold": 120,
            "prize": 220,
            "uid": 1002922
        }
        with self.assertRaises(RuntimeError):
        	rk.push_in(user_1)
        	rk.plugin(add_profit)


    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
