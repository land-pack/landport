from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route('/')
def hello():
	return 'hello'

@app.route('/login/<name>')
def get_name(name):
	print 'client name is %s' % name
	return 'ok'


if __name__ == '__main__':
	app.run(port=5000, debug=True)