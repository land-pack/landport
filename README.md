# Landport

Python online game framework (zeromq + redis + flask + gevent + tornado)


Installation
------------

You can install this package as usual with pip:

    pip install landport

Example
-------

	cd landport/demo
	python manage.py

And then use a websocket client put the below url in it!

	ws://127.0.0.1:9922/ws?node=123&room=4526&uid=455

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
