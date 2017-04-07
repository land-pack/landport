import requests

uid = raw_input("Please input yor uid:")

r = requests.get('http://localhost:9933/join?uid=%s' % uid)
if r.status_code == 200:
	pass
else:
	pass

