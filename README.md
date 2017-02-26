# Landport

Python online game framework (zeromq + redis + flask + gevent + tornado)


Installation
------------
Create your running environment:
	virtualenv venv

You can install this package as usual with pip:

    pip install landport

Example
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

Function
-------

	>> chat
	>> rank
	>> join/leave room
	>> ...

Why it?
------

I can't find any useful game server framework, so i decide build myself! it's also need you help ! let's build it together!
