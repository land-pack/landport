import requests
import time


start = time.time()

for i in range(1000):
	r = requests.get('http://127.0.0.1:9933/?num1=123&num2=456')
	# print r.content

end = time.time()

print 'time cost:%6f' % (end - start)