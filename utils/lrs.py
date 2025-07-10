from .tuplestorage import TupleStorage
from .trie import Trie
from utils import helper

from .helper import gcdlist

class lrs:
	# LRS

	order=0
	initial = []
	recurrence = []

	def __init__(self, order, initial, recurrence):
		self.order = order
		self.initial = initial
		self.recurrence = recurrence

	def equals(self, other):

		if self.order != other.order:
			return False

		if any([x!=y for x,y in zip(self.initial,other.initial)]):
			return False
		
		if any([x!=y for x,y in zip(self.recurrence,other.recurrence)]):
			return False

		return True


	def getReverseLRS(self):
		# note does not do the normalisation step so the result is a rational LRS (but probably represented with floats)
		# note does not do shift. So position 0,...,lrs.order corresponds with lrs.order,...,0
		# call .shift(lrs.order) for positions 0,...lrs.order to correspond to 0,...,-lrs.order
		print("------ FLOATING POINTS LIKELY ------ are you sure you want to call this?")
		order =self.order
		initial = list(reversed(self.initial))
		head = self.recurrence[-1]
		recurrence = [-a/head for a in reversed(self.recurrence[:-1])] + [1/head]
		return lrs(order, initial, recurrence)

	def getNormalisedReverseLRS(self):
		# note does do the normalisation step
		# preserves zeros only
		# note does not do shift. So position 0,...,lrs.order corresponds with lrs.order,...,0
		# call .shift(lrs.order-1) for positions 0,...lrs.order to correspond to 0,...,-lrs.order
		
		order =self.order
		head = self.recurrence[-1]
		headMag = abs(head)
		headSign = helper.sign(head)
		recurrence = [-a*headSign*headMag**(i) for i,a in enumerate(reversed(self.recurrence[:-1]))] + [headSign*headMag**(order-1)]
		initial = [(headMag**i) * x for i,x in enumerate(reversed(self.initial))]
		return lrs(order, initial, recurrence)

	def getShiftedNormalisedReverseLRS(self):
		# note does do the normalisation step
		# preserves zeros only
		# note does  do shift.
		# FURTHER, it renormalises the initial to be as small as appropriate.

		from . import subsequences
		head = abs(self.recurrence[-1])
		lrs = self.getNormalisedReverseLRS().shift(self.order-1)
		# print(lrs.initial)
		
		lrs.initial = subsequences.resolveInitial(lrs.initial, head**(self.order-1))
		return lrs

	def getReducedLrs(self):
		mygcd = gcdlist(self.initial)
		newinitial = [u // mygcd for u in self.initial]
		return lrs(order = self.order, initial = newinitial, recurrence = self.recurrence)

	def __str__(self):
		return "u_{n} = " +  " + ".join([str(x) +"u_{n-" + str(i+1) + "}" for i,x in enumerate(self.recurrence)])+ "\n" + "initial: " + ", ".join([str(x) for x in self.initial])

	def negStr(self):
		return "u_{n} = " +  " + ".join([str(x) +"u_{n+" + str(i+1) + "}" for i,x in enumerate(self.recurrence)])+ "\n" + "initial (index: 0,-1,-2, ...): " + ", ".join([str(x) for x in self.initial])

	def shift(self,n):
		firstorderplusn = self.listn(n+self.order)
		return lrs(self.order, firstorderplusn[-self.order:],self.recurrence)

	def nextTupleStorage(self, tpl, modulo = False):
		nxt= 0
		for i in range(self.order):
			nxt = nxt + self.recurrence[i]*tpl.getPosition(-1-i)

		if modulo != False:
			nxt = nxt % modulo
		tpl.shift(nxt)
		return nxt


	def listn(self,n,modulo=False):
		return list(self.getTo(n,modulo))

	def getTo(self,n, modulo = False):
		if modulo:
			initial = [x % modulo for x in self.initial]
		else:
			initial = self.initial.copy()

		for i in range(min(self.order,n)):
			yield(initial[i])

		u = TupleStorage(initial)
		i = self.order
		while i < n:
			nxt = self.nextTupleStorage(u,modulo)
			yield nxt
			if (i & (i-1) == 0) & i > 1000:
				print("Still generating getTo",n, "at", i, nxt)
				pass
			i+=1

	def getPos(self,n, modulo = False):
		if modulo:
			initial = [x % modulo for x in self.initial]
		else:
			initial = self.initial.copy()

		if n < self.order:
			return initial[n]

		u = TupleStorage(initial)
		i = self.order
		while i <= n:
			nxt = self.nextTupleStorage(u,modulo)
			if (i & (i-1) == 0) & i > 1000:
				print("Still generating getPos",n, "at", i, nxt)
				pass
			i+=1
		return nxt

	def getCompanionMatrix(self):
		# Returns python list of lists
		matrix = []
		matrix.append(self.recurrence)
		for i in range(self.order-1):
			matrix.append([1 if j == i else 0 for j in range(self.order)])
		return matrix


	def checkForZeroUpTo(self, n, checkInitial = True):
		
		initial = self.initial.copy()

		if checkInitial:
			for i in range(min(self.order,n)):
				if initial[i] == 0:
					return True,i

		u = TupleStorage(initial)
		i = self.order
		while i < n:
			nxt = self.nextTupleStorage(u)
			if nxt == 0:
				return True,i
			i+=1
		return False, None


	def moduloChecker(self, modulo):
		# low memory modulo checker
		# guesses where the first repetition is and then waits to see it again
		# not necessarily the first repetition
		multiplier = 5

		while True:
			first = [x % modulo for x in self.listn(self.order*multiplier)]
			searching = TupleStorage(first[-self.order:])

			print("modulo", modulo, "multiplier",multiplier,"searchingFor", searching)
			maxsearchlength = modulo**self.order + self.order

			u = TupleStorage(first[-self.order:])
			containsZero = False
			i = 0
			while i < maxsearchlength:
				i+=1
				nxt = self.nextTupleStorage(u,modulo)
				if nxt ==0 :
					containsZero = True
				if u.equals(searching):
					print("modulo", modulo, "steps", i, "found", u, "containsZero", containsZero)
					return (modulo, containsZero, i, u)
			print("modulo", modulo,"failedToFind", searching)
			multiplier *= 2


	def getRepitionModulo(self,modulo, options = None):
		# if you know it is periodic, not eventually periodic, this is not the method for you!

		seen = Trie()
		u = TupleStorage([x % modulo for x in self.initial])
		
		seen.add(u.asTuple(),self.order - 1)
		i = self.order
		while True:
			nxt = self.nextTupleStorage(u, modulo)

			if seen.contains(u.asTuple()):
				# print("repetition of", tuple(u), " between ", seen[tuple(u)], i)
				return (u.asTuple(),  seen.get(u.asTuple()), i, u.asList())
			seen.add(u.asTuple(), i) 
			i+=1

			# just a message to make it clear that it is still doing something
			# outputs if i = 2^k for some k
			if options == None or options.get("print"):
				if (i & (i-1) == 0) and i > 255:
					print("Still computing repetition at step", i)
					pass

	def getRepitionModuloLength(self, modulo, ToKill, KillBound = -1, options = None):
		# If ToKill=False then you *must* know that it is periodic modulo modulo, not just eventually periodic!
		# This version returns -1 when the period gets too large!

		first = self.listn(self.order,modulo)
		initial = TupleStorage(first)
		current = TupleStorage(first)

		i = 0
		while not ToKill or i <= KillBound:
			i += 1
			nxt = self.nextTupleStorage(current, modulo)

			if current.equals(initial):
				return i
		
			# just a message to make it clear that it is still doing something
			# outputs if i = 2^k for some k

			if options == None or options.get("print"):
				if (i & (i-1) == 0):
					print("Still computing repetition at step", i)
					pass
		
		return -1

	def getRepitionModuloList(self, modulo):
		# You *must* know that it is periodic modulo modulo, not just eventually periodic!

		listOfValues = self.listn(self.order,modulo)

		# once we see the listOfValues values again we can stop and we have periodic behaviour
		searching = TupleStorage(listOfValues)
		current = TupleStorage(listOfValues)
		while True:
			nxt = self.nextTupleStorage(current,modulo)
			listOfValues.append(nxt)
			if current.equals(searching):
				return listOfValues


	def lastTerm(self):
		return self.recurrence[-1]


	def isSimple(self):
		from . import subsequences
		return subsequences.isSimpleSage(self)


	def isDegenerate(self):
		from . import subsequences
		return subsequences.isDegenerate(self)


