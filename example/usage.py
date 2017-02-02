from landport.room import RoomManager
from flask import Flask
from flask import render

app = Flask(__name__)
manager = RoomManager(room_size=9)

@app.route("/api/join")
def join(user_name):
	room_name = manager.book(user_name)
	return usjon(room_name)

