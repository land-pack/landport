from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit, leave_room, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
app.debug=True

@app.route("/")
def index():
	return render_template("index.html")

def ack():
	print 'message are received'

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    # send('echo:%s' % message)
    json = {"name":message}
    emit('message', json, callback=ack)



@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    print 'username=%s has leave' % username
    leave_room(room)
    send(username + ' has left the room.', room=room)

if __name__ == '__main__':
    socketio.run(app)