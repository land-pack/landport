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

.. automodule:: landport
   :members:

