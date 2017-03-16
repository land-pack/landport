import time
import redis  
  
rc = redis.Redis(host='127.0.0.1')
test_max = 100000
# for redis 
start = time.time()
for i in xrange(test_max):
	rc.set(i, i, ex=60)


end = time.time()
print 'redis set for %s -- cost:%s' % (test_max, end - start)
# for python dict
start = time.time()
d = {}
for i in xrange(test_max):
	d[i] = i

end = time.time()
print 'python dict set for %s -- cost:%s' % (test_max, end - start)