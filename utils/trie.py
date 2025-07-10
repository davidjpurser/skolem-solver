
class Trie:
	# Stores a set of tuples
	# Stores tuples in a tree
	# Testing whether tuple in set should be O(tuple_size) not O(set_size)


	dic = dict()
	def __init__(self):
		self.dic = dict()


	def __str__(self):
		return self.dic.__str__()

	def add(self, key,value):


		if self.contains(key):
			return False

		key = list(key)
		currdic = self.dic
		for i,x in enumerate(key):
			if x in currdic:
				currdic = currdic[x]
			else:
				currdic[x] = self.make(key[i+1:], value)
				return True

		
	def make(self,key,value):
		if len(key) ==0 :
			return {"value": value}
			
		currdic = dict()
		currdic[key[0]] = self.make(key[1:],value)
		return currdic
		


	def contains(self, value):


		value = list(value)
		currdic = self.dic

		for i,x in enumerate(value):
			if x in currdic:
				currdic = currdic[x]
			else:
				return False

		return "value" in  currdic



	def get(self, value):


		value = list(value)
		currdic = self.dic

		for i,x in enumerate(value):
			if x in currdic:
				currdic = currdic[x]
			else:
				return False

		return currdic["value"]