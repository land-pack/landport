=============
 Quick Start
=============

Installing
=============

Install with ``pip``::

  $ pip install landport


Usage
=============
Ranklist using::

  from landport.core.rank import RanklistBase as Ranklist

One line code can import all your need, and then declare a Ranklist instance. Rank list need to cache last rank record, so you should declare a redis connect handler before declare a Ranklist instance.

::

  import redis
  r = redis.Redis('localhost')

Now, you can declare a Ranklisk instance.

::

  rk = Ranklist('last_ranklist_cache', r)

Once you get a rank list instance, you can push you data in, assume you have some data element as below show:

::

  frank = {
    "english": 120,
    "math":99,
    "uid": 1002222
  }

And then, you can easily push it in your rank list.

::

  rk.push_in(frank)

You may have a lot of data from your database, so you can easy push it in by a loop. also can do it by a `push_many([...])` in the future.

::

  for i in my_data:
     rk.push_in(i)

For now, we got data in our Ranklist, we can sort the element and fetch what we care.

::
  
  top10 = rk.top(10)

As we can see, one line code will get data which we want.

.. automodule:: landport
   :members:

