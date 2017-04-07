import time

def sec_to_time(s):
	m, s = divmod(s, 60)
	h, m = divmod(m, 60)
	return '{}:{}'.format(h,m)

def time_to_sec(t):
    h,m,s = t.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)



def timestamp_to_datetime(timestamp, fmt=None):
	"""
	fmt
	"""
	time_local = time.localtime(timestamp)
	if fmt:
		dt = time.strftime("{}".format(fmt),time_local)
	else:
		dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
	return dt

def time_offset(timestamp, h=None, m=None, s=None):
	if h:
		timestamp += h*60*60
	if m:
		timestamp += m*60
	if s:
		timestamp += s
	return timestamp

if __name__ == '__main__':
	s = 3600
	t = sec_to_time(s)
	print(t)
	tt = '1:1:40'
	ss = time_to_sec(tt)
	print(ss)
	print('*'*100)
	t = time.time()
	print timestamp_to_datetime(t)
	t = time_offset(t, 24, 1,2)
	print timestamp_to_datetime(t, "%m-%d %H:%M")

