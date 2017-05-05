a= [
	{
		"uid":"123",
		"money":1200
	},
	{
		"uid":"234",
		"money":450
	}
]

def cut_data(lst, money_limit=500):
	new_lst = []
	for i in lst:
		money = i.get("money")
		if  money > money_limit:
			moneys = [money_limit for j in xrange(money/money_limit)]
			remainder = money % money_limit
			moneys.append(remainder)
			for j in moneys:
				d = {
					"uid": i.get("uid"),
					"money":j
				}
				new_lst.append(d)
		else:
			new_lst.append(i)
	return new_lst

if __name__ == '__main__':
	n = cut_data(a)
	print(n)
	