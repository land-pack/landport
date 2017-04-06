def filter_a(lst):
	for i in lst:
		if i in ['foo','bar']:
			return True
		return False

lst = ['sfoo','sbar','jack','frank']
print(filter_a(lst))

def filter_b(lst):
    return bool(set(lst) - set(['foo','bar']))

print(filter_b(lst))

