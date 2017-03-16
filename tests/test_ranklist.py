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

if __name__ == '__main__':
    rk = Ranklist('last_ranklist_cache', r)
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


    rk.sort_by("profit").add_rank().add_gift(your_mongodb_gift_configure).add_value_from(fetch_from_your_mysql_db_by_uid, 'uid', 'name').add_trend()

    print(rk.rank())
    print("=" * 100)
    rk2 = Ranklist('last_ranklist_cache', r)
    rk2.push_in(user_a)
    user_b = {
        "gold": 120,
        "prize": 520,
        "uid": 1002923
    }
    rk2.push_in(user_b)
    rk2.push_in(user_c)
    rk2.sort_by("profit").add_rank().add_gift(your_mongodb_gift_configure).add_value_from(fetch_from_your_mysql_db_by_uid, 'uid', 'name').add_trend()
    print(rk2.rank())
