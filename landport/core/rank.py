class Ranklist(object):


	def __init__(self, name, age, score):
		self.name = name
		self.age = age
		self.score = score

	def __lt__(self, other):	
		if self.name == other.name:
			if self.age == other.age:
				return self.score < other.score
			return self.age < other.age
		return self.name < other.name

	def __gt__(self, other):
		if self.name == other.name:
			if self.age == other.age:
				return self.score > other.score 
			return self.age > other.age 
		return self.name > other.name

	def __str__(self):
		return '({}-{}-{})'.format(self.name, self.age, self.score)

	def __repr__(self):
		return self.__str__()

class RankManager(object):
	def __init__(self, rank, prize):
		pass

if __name__ == '__main__':
	p1 = Ranklist(1, 2, 2)
	p2 = Ranklist(1, 2, 3)
	p3 = Ranklist(1, 2, 1)
	p4 = Ranklist(1, 4, 3)
	p5 = Ranklist(4, 2, 3)
	p6 = Ranklist(4, 2, 3)
	p = [p1, p2, p3, p4, p5, p6]
	print(p)
	pp = sorted(p)
	print(pp)