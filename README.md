# Landport

Python online game framework (zeromq + redis + flask + gevent + tornado). you can easy build a multi-players video/web/mobile game ~:)


Installation
------------
Create your running environment:
	
	# pick a path , example your home path
	cd ~
	virtualenv venv

You can install this package as usual with pip:

    pip install landport

Game Room Example
-------

	cd landport/demo

	# open first terminal run a game node server
	python manage.py 
	# open second terminal run a game room server
	python room.py
	# open thrid terminal run a client-side/
	python app.py

First at first you need apply a game room, so visit the roomserver by:
	
	http://x.x.x.x:xx/join?uid=xx

And then you will got something response , there are include your `created`,`node`,`ip`,`port`,`room`,`uid`. Put those on a websocket client as below url show!
	
	ws://x.x.x.x:xx/ws?ip=x.x.x.x&port=xx&node=xx&room=xx&created=xxx&uid=xx

You should change your uid when you open a new client each time!

Rank List Example
------
	# plugin function declare ....
	def add_score(d):
	    money = d.get("total_money") - d.get("cost_money")
	    d.update({"score": money})	
	
	def add_username(d):
	    uid = d.get("uid")
	    username = fetch_username_from_your_database_by(uid)
	    d.update({"username": username})
	
	# Ranklist instance declare ...
	r = redis.Redis("127.0.0.1", 6379, 0)
	rk = Ranklist('ranklist_cache', r)
	
	# install your plugin function ...
    rk.plugin(add_profit)
    rk.plugin(add_username)
	for item in your_user_join_list:
		"""
		item should be a dict type, structure as below show:
		{
			"uid":"123",
			"total_money":1990,
			"cost_money":889
		}
		"""
		rk.push_in(item)
	
	rk.sort_by("score").add_rank(conflict=False)
	# get your rank list, the item have some new field name as `score`
	# But we still need more , like do i go forward or retreat ...
	rk.sort_by("profit").add_rank(conflict=False).add_trend()
	#normally we need to show user what gift can get, so we also can do it easily !
	gift_map = {
		"1":{ "name":"iPhone 7 plug", ...},
		"2~4": {"name":"ipod"}
	}
	rk.sort_by("profit").add_rank(conflict=False).add_trend().add_gift(gift_map))
	# finnaly, you may want to know how to get the rank list back! if you only care first 15 one!
	ranklist_result = rk.top(15)		
	# fore more see my blog!
Function
-------

	>> chat
	>> rank
	>> join/leave room
	>> ...

Why it?
------

I can't find any useful game server framework, so i decide build myself! it's also need you help ! let's build it together!
