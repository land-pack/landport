from landport import Landport
from landport.room import join_room, leave_room, rooms, close_room
from landport.ttl import TTL 
from landport.websocket import WebSocket
from landport.event import checker
from landport.views import View 
from landport.robot import Robot



app = Landport()
ttl_hb = TTL(app=app, name='heartbeat', expire=120)
ttl_op = TTL(app=app, name='operate', expire=180)
BaseView = View(app=app, namespace='/', data_type=str)

class MyView(BaseView)
	def ping(self):
		ttl_hb.update(self)
		return "p"

	def do_thing(self):
		ttl_op.update(self)
		return "xxx"

	def default(self):
		return "default"


@app.ws("/hello")
class MyWebSocket(WebSocket):
	def open(self)
		join_room(self)

	def on_message(self, msg):
		self.write_message(my_view.dispatch(self, msg))

	def on_close(self)
		leave_room(self)


if __name__ == '__main__':
	app.run(debug=True)