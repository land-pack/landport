import redis  
  
rc = redis.Redis(host='127.0.0.1')  
  
ps = rc.pubsub()  
  
ps.subscribe(['foo', 'bar']) 
  
for item in ps.listen():  
  
    if item['type'] == 'message':  
  
        print item['data']