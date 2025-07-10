


class LinearSet:
	# a linear set consisting of start + period N
	# May also store linear set of type Z and Zne0

	start = 0
	period = 1
	typ = 'N'

	def __init__(self, start, period):
		self.start = start
		self.period = period

	def setType(self, typ):
		self.typ = typ


	def mapInside(self, inside):
		return LinearSet(inside.start + self.start * inside.period, self.period * inside.period)

	def mapNumberInto(self,number):
		# gets the number th entry of the set
		return self.start+self.period*number

	def __str__(self):

		if self.typ == "N": 
			return "(" + str(self.start) + "+ " + str(self.period)  +"N)"
		if self.typ == "Z": 
			return "(" + str(self.start) + "+ " + str(self.period)  +"ℤ)"
		if self.typ == "Zne0": 
			return "(" + str(self.start) + "+ " + str(self.period)  +"ℤ<sub>≠0</sub>)"
	
	def __repr__(self):
		return self.__str__()

	def toJSON(self):
		return self.__str__()

	def contains(self, number):
		# check if a number is in the set
		remainder = number - self.start
		if remainder == 0:
			return True

		return remainder %self.period ==0 and (helper.sign(remainder) == helper.sign(self.period))

	def firstN(self, n):
		# get the first n values of the set.
		# lazy generator
		st = self.start
		yield st

		for i in range(n-1):
			st += self.period
			yield st			

	def normalise(self, period):
		# change the period
		# lazy generates several new linear sets (the union of which is equivalent to this set)

		if period % self.period != 0:
			raise ValueError('The proposed period is not a multiple of the current period')

		for i in range(0, period, self.period):
			yield LinearSet(self.start + i,period)


# Testings
if __name__ == "__main__":

	ls = LinearSet(2,3)
	ls2 = LinearSet(4,5)

	print(ls,ls2)

	print(ls.mapInside(ls2))
	print(ls2.mapInside(ls))


	ls = LinearSet(40,5)
	ls2 = LinearSet(6,2)

	print(ls,ls2)

	print(ls.mapInside(ls2))
	print(ls2.mapInside(ls))


	print(ls.contains(40))
	print(ls.contains(45))
	print(ls.contains(50))
	print(ls.contains(35))
	print(ls.contains(41))
	print(ls.contains(0))


	ls = LinearSet(40,-5)
	print(ls)
	print(ls.contains(40))
	print(ls.contains(45))
	print(ls.contains(50))
	print(ls.contains(35))
	print(ls.contains(41))
	print(ls.contains(0))


	ls = LinearSet(13,4)
	print(list(ls.firstN(5)))

	ls = LinearSet(2,5)
	print(list(ls.normalise(25)))

