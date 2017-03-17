import redis
from landport.core.rank import RanklistBase as Ranklist

r = redis.Redis("127.0.0.1", 6379, 0)

def fetch_from_your_mysql_db_by_uid(uid):
    d = {
        "1002922": "frank",
        "1002923": "jack",
        "1002924": "pig"
    }
    return d.get(uid)

your_mongodb_gift_configure = {
        "1": {"xx": "yy"},
        "2~3": {"22": 33}
    }

def add_profit(d):
    p = d.get("prize") - d.get("gold")
    d.update({"profit": p})

def add_userinfotmation(d):
    uid = d.get("uid")
    print('xxxx%s' % type(uid))
    username = fetch_from_your_mysql_db_by_uid(uid)
    d.update({"username":username})

if __name__ == '__main__':
    rk = Ranklist('last_ranklist_cache', r)
    rk.plugin(add_profit)
    rk.plugin(add_userinfotmation)
    user_a = {
        "gold": 120,
        "prize": 220,
        "uid": 1002922
    }
    rk.push_in(user_a)
    user_b = {
        "gold": 120,
        "prize": 320,
        "uid": 1002923
    }
    rk.push_in(user_b)
    user_c = {
        "gold": 120,
        "prize": 420,
        "uid": 1002924
    }

    rk.push_in(user_c)


    rk.sort_by("profit").add_rank().add_gift(your_mongodb_gift_configure).add_trend()

    print(rk.top())
    print("=" * 100)
    rk2 = Ranklist('last_ranklist_cache', r)
    rk2.plugin(add_profit)
    rk2.plugin(add_userinfotmation)
    rk2.push_in(user_a)

    user_b = {
        "gold": 120,
        "prize": 520,
        "uid": 1002923
    }
    rk2.push_in(user_b)
    rk2.push_in(user_c)
    rk2.sort_by("profit").add_rank().add_gift(your_mongodb_gift_configure).add_trend()
    print(rk2.top(2))
    print("=" * 100)
    print("about me")
    print(rk2.about_me('1002922'))
