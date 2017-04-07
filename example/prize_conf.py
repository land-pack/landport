a = {
	"1":"hello world",
	"2~5":"range between 2~5",
	"6~7":"range between 6~7"
}

def extend_dict(d):
	"""
	Input:
		a = {
			"1":"hello world",
			"2~5":"range between 2~5",
			"6~7":"range between 6~7"
		}
	Output:
		{
		    '1': 'helloworld',
		    '3': 'rangebetween2~5',
		    '2': 'rangebetween2~5',
		    '5': 'rangebetween2~5',
		    '4': 'rangebetween2~5',
		    '7': 'rangebetween6~7',
		    '6': 'rangebetween6~7'
		}
	"""
	new_d = {}
	for k, v in d.iteritems():
		if '~' in k:
			start, end = k.split('~')
			keys = range(int(start), int(end)+1)
			for i in keys:
				new_d.update({
						str(i):v 
					})
		else:
			new_d.update({
				k:v
				})
	return new_d

if __name__ == '__main__':
	b = extend_dict(a)
	print(a)
	print(b)
