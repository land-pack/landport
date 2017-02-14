def split_order(lst, copies=4):
	length = len(lst)
	step = length / copies
	l = []
	for i in range(copies):
		end_ = step * i
		if i == copies-1:
			l.append(lst[end_:])
		else:
			l.append(lst[end_:end_+step])
	return l

if __name__ == '__main__':
	l =split_order([1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,5,8,7,99])
	print l