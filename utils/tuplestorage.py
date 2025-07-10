""" 
Essentially a fixed-length queue. 
Shift(x) is equivalent to append(x), pop(0).
Stores a tuple that will be shifted many times, without changing much memory allocations. 
"""

class TupleStorage:

	length = 0
	start = 0
	lst = []

	def __init__(self, lst):
		self.length = len(lst)
		self.lst = lst.copy()
		self.start = 0

	def incrementPosition(self, start):
		return (start + 1)% self.length

	def shift(self, value):
		self.lst[self.start] =value
		self.start = self.incrementPosition(self.start)


	def asList(self):
		lst = []
		position = self.start
		for _ in range(self.length):
			lst.append(self.lst[position])
			position = self.incrementPosition(position)
		return lst

	def asTuple(self):
		return tuple(self.asList())

	def getPosition(self, position):
		return self.lst[(self.start + position) % self.length]

	def __str__(self):
		return self.asList().__str__()

	def equals(self, other):
		if self.length != other.length :
			return False

		lst = []
		position = self.start
		position2 = other.start
		for _ in range(self.length):
			if self.lst[position] != other.lst[position2]:
				return False
			position = self.incrementPosition(position)
			position2 = other.incrementPosition(position2)
		return True

