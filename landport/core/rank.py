def cmp_cir(a, b):
	if a == b:
		pass



class Ranklist(object):


	def __init__(self, name, *args,**kwargs):
		self.name = name
		self.__dict__ = kwargs
		self.args = args


	def __lt__(self, other):	
		for k in self.args:
			other_value = getattr(other, k)
			v = getattr(self, k)
			if v == other_value:continue
			return v < other_value
		return True


	def __str__(self):
		return '(rank_list:{})'.format(self.name)

	def __repr__(self):
		return self.__str__()

class RankManager(object):
	def __init__(self, rank, prize, my=None):
		pass

	def add_profit(self, lst):
		"""
		Example:
			[
				{"gold":200, "prize":400},
				{"gold":100, "prize":600}
			]
		Return:
			[
				{"gold":200, "prize":400, "profit":200},
				{"gold":100, "prize":600, "profit":500}
			]
		"""
		pass

	def add_total_gold(self):
		pass

	def add_username(self):
		pass

	def add_rank(self):
		pass

	def add_prize_level(self):
		pass

	def add_prize(self):
		pass

	
	





if __name__ == '__main__':
	p1 = Ranklist('jack' ,'chinese', 'math', chinese=95, math=88)
	p2 = Ranklist('lisa' ,'chinese', 'math', chinese=96, math=81)
	print p1 > p2
	p1 = Ranklist('jack' ,'math', 'chinese', chinese=95, math=88)
	p2 = Ranklist('lisa' ,'math', 'chinese', chinese=96, math=81)
	print p1 > p2
	d1 = {"a":23,"b":12,"c":88,"d":11}
	d2 = {"a":3,"b":22,"c":88,"d":11}
	p1 = Ranklist('ww', 'a','c','b', **d1)
	p2 = Ranklist('vv', 'a','c','b', **d2)
	print p1 > p2 
	# p2 = Ranklist(1, 2, 3)
	# p3 = Ranklist(1, 2, 1)
	# p4 = Ranklist(1, 4, 3)
	# p5 = Ranklist(4, 2, 3)
	# p6 = Ranklist(4, 2, 3)
	# p = [p1, p2, p3, p4, p5, p6]
	# print(p)
	# pp = sorted(p)
	# print(pp)