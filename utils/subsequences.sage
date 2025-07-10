import sys
from .lrs import lrs
from . import lrsreader 
from .linearset import LinearSet
import fileinput

# Methods for making subsequences 


def getCompanionMatrix(lrs):
	# Find the companion matrix
	matrix = lrs.getCompanionMatrix()
	A = MatrixSpace(IntegerRing(),lrs.order)(matrix)
	return A

def getAlgebraicCompanionMatrix(lrs):
	# Find the companion matrix over algebraic numbers
	matrix = lrs.getCompanionMatrix()
	A = MatrixSpace(QQbar,lrs.order)(matrix)
	return A


def charpolylrs(lrs):
	Z.<t> = ZZ[]
	return Z(([1] + [-a for a in lrs.recurrence])[::-1])


def getRecurrence(matrix):
	# get the recurrence from a matrix
	f = matrix.charpoly()
	lrsrecurrence = [-x for x in reversed(f.list())][1:]
	return lrsrecurrence

def powermatrix(matrix, power):
	# take the power of a matrix
	return matrix^power

def getInitial(first, linearset, order):
	#get the initial set for a new lrs corresponding to the subsequence according to the linear set 
	# should be combined with a companion matrix taking linearset.period as the power
	return [first[i] for i in linearset.firstN(order)]

def resolveInitial(lst,factor):
	return [Integer(Integer(x)/Integer(factor)) for x in lst]


def factorIntoSteps(m):
	# This function has as input a positive integer m such that u_0 = 0 and u_{nm} != 0 for all n >= 1
	# It outputs a list of list of classes [(L, [a,...,])... ] such that a + b n needs to be checked for all n
	ListOfClasses = []
	Factorization = factor(m)[::-1] # Reversing for optimization
	Currentb = 1
	for primepower in Factorization:
		p = primepower[0]
		for power in range(primepower[1]):
			Newb = Currentb * p
			ListOfClasses.append((Newb, [i*Currentb for i in range(1, p)]))
			Currentb = Newb
	return ListOfClasses

def findBetterBoundRootOfUnity(n):
	# Computes a better bound on the largest possible root of unity.
	Factorization = factor(n)
	Newn = 1
	for Factor in Factorization:
		p, mult = Factor[0], Factor[1]
		Newn *= p^floor(log((mult + 1)/(p-1), p)+1)
	# Include the second roots of unity if they are there yet
	if Newn % 2 == 1:
		Newn *= 2
	return Newn
		
def isDegenerate(lrs):
	matrix = lrs.getCompanionMatrix()
	A = MatrixSpace(IntegerRing(),lrs.order)(matrix)
	
	f = A.charpoly()
	factors = [g[0] for g in list(factor(f))] 
	K.<t> =QQ[]
	for f in factors: 
		x = K(f)
		# I hope this is correct!
		L.<a> = NumberField([y[0] for y in factor(x)])
		L.<b> = L.absolute_field()
		K.<t> = L[]

	disc = abs(L.discriminant())

	# print("disc", disc)

	disc = findBetterBoundRootOfUnity(disc)

	# print("Better bound for roots of unity", disc)
	
	mt = getAlgebraicCompanionMatrix(lrs)
	roots = [f[0] for f in mt.charpoly().roots()]
	for i in range(len(roots)):
		for j in range(i):
			r1 = roots[i]
			r2 = roots[j]
			rat= r1/r2
			powered = rat^disc
			if ( powered == 1):
				print("ratio of roots", r1,r2, rat, "is rou", rat^disc)
				return True
	return False

	

def isSimpleSage(mylrs):
	f = charpolylrs(mylrs)
	return gcd(f, f.derivative()).degree() == 0



def minimizeLRS(mylrs):
	# Find the minimal recurrence for a given LRS
	# Please do not input the zero LRS!

	firstFewValues = mylrs.listn(mylrs.order * 2)

	for i in range(mylrs.order, 0, -1):

		newMatrix = matrix([firstFewValues[j : i + j] for j in range(i)])

		# if linearlyIndependent the correct order is found
		if newMatrix.det() != 0:
			
			recurrence = list(newMatrix.inverse() * vector(firstFewValues[i : 2*i]))
			
			return lrs(i, firstFewValues[:i], recurrence[::-1])

	



### Testing
if __name__ == "__main__":

	mylrs = lrsreader.readLRS(lines)

	print(mylrs)
	print(mylrs.listn(10))

	matrix = getCompanionMatrix(mylrs)
	matrix2 = powermatrix(matrix,2 )
	print(matrix2)
	lrsrecurrence = getRecurrence(matrix2)
		
	print(mylrs.recurrence, lrsrecurrence)

	len = 40
	first = mylrs.listn(len)
	alternate = [first[i] for i in range(0,len,2)]

	print("first",first)
	initial = getInitial(first, LinearSet(1,2), mylrs.order)
	print("alternate", alternate)
	print("initial", initial)

	secondlrs = lrs(mylrs.order, alternate[:mylrs.order] ,lrsrecurrence)
	print(secondlrs)
	print(secondlrs.listn(20))
