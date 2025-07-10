from utils.lrs import lrs
from utils.subsequences import getCompanionMatrix
from utils.helper import optionalprint

# Computes minimum L such that lambda^L = 1 mod p LRS modulo p (fast). 
def ComputePeriod(f, p):
	Fpt.<t> = FiniteField(p)[]
	ff = Fpt(f)
	factorf, myPeriods = [fac for fac in factor(ff)], []
	if max([fac[1] for fac in factorf]) > 1:
		N = 50
		for tup in f.discriminant().factor():
			if p == tup[0]:
				N += tup[1]	
		ZZp.<y> = Zp(p, N)[]
		for fac in ZZp(f).factor():
			myPeriods.append(p^fac[0].degree() - 1)
	else:
		for fac in factorf:
			q = p^fac[0].degree()
			Fqt.<t2> = FiniteField(q)[]
			myPeriods.append(Fqt(fac[0]).roots()[0][0].multiplicative_order())
	return lcm(myPeriods)


# Helper function to compute a S >= 1 such that u_{Sn} != 0
# Only use this function when all characteristic roots lie in Q_p! 

def FindStepforSplittingp(mylrs, options, p, ToKill = False, KillBound = 0, N = 100):
	# N is the accuracy of the p-adic computations

	# The prime 2 needs a special treatment
	if p == 2:
		extraCoeff = 2
	else:
		extraCoeff = 1

	# f is the characteristic polynomial of the LRS.
	Z.<t> = ZZ[]
	f = Z(([1] + [-a for a in mylrs.recurrence])[::-1])

	L = ComputePeriod(f, p) * extraCoeff

	# Little protection against getting overly big jumps
	# The second argument describes the biggest allowed period
	optionalprint(options, lambda: "prime: " + str(p) + " period: " + str(L) + " Splitting case")
	if L == -1:
		return 0
	QpN = Qp(p, N)
	Q.<t>= QpN[]

	Qpf = Q(([1] + [-a for a in mylrs.recurrence])[::-1])
	MyRoots = [a[0] for a in Qpf.roots()]
	if len(MyRoots) != mylrs.order:
		optionalprint(options, lambda: "Too few roots: Either the LRS is not simple or the p-adic accuracy is too low")
		return 0

	# Compute the coefficients of the polynomial exponential sum
	VanDerMonde = sage.matrix.special.vandermonde(MyRoots).transpose()
	Coefficients = 	VanDerMonde^-1 * vector(mylrs.initial)

	# Alla will be the list with v_p(a_j) for all possibly relevant a_j.
	Alla = []
	
	for k in range(mylrs.order * 2):
		a = QpN(0)
		for i in range(mylrs.order):
			a += Coefficients[i] * log(MyRoots[i]**L)^k/factorial(k)
		Alla.append(valuation(a))
	optionalprint(options, lambda: "The first 2k valuations of the a_j for " +str(p) +  ": " + str(Alla))
	# If the first k a_j are zero, then the sequence is the zero sequence. So, with high enough precision, this won't happen!
	for i in range(k):
		if Alla[i] == N:
			continue
		NewValuations = [Alla[j] - Alla[i] for j in range(i+1, i + mylrs.order)]
		mypower = 0
		
		while True in [a <= 0 for a in NewValuations]:
			mypower += 1
			NewValuations = [NewValuations[j] + j + 1 for j in range(mylrs.order - 1)]
		return L* p^mypower
		# return (L * p^mypower, L, p, mypower)
	return 0

# Helper function to compute a S >= 1 such that u_{Sn} != 0
# This version can be used for all polynomials!
def FindStepforSmallp(mylrs, options, p, ToKill = False, KillBound = 0, N = 100):

	# N is the accuracy of the p-adic computations
	maxk = N

	# The prime 2 needs a special treatment
	if p == 2:
		extraCoeff = 2
	else:
		extraCoeff = 1

	# f is the characteristic polynomial of the LRS.
	Z.<t> = ZZ[]
	f = Z(([1] + [-a for a in mylrs.recurrence])[::-1])

	L = ComputePeriod(f, p) * extraCoeff

	# Little protection against getting overly big jumps
	# The second argument describes the biggest allowed period
	optionalprint(options, lambda:"prime: " + str(p) + " period: " + str(L) + " Non-splitting case")
	if L == -1:
		return 0
	

	cmp = matrix(mylrs.getCompanionMatrix())
	B = (cmp^L - 1)/p
	v = vector([0 for i in range(mylrs.order-1)] + [1])
	w = vector(mylrs.initial[::-1]).column()


	d = [v * w]
	Bi = v
	for _ in range(1, maxk):
		Bi = Bi *  B
		d.append(Bi * w)

	# d = [v * B^i * w for i in range(maxk)] # recomputing B^i each step is not great
	MyQp = Qp(p, N)
	Alla = []
	
	for j in range(2 * mylrs.order):
		a = 0
		for k in range(j, maxk):
			a += -stirling_number1(k, j)*(-1)^j * p^k * d[k][0] / factorial(k)
		if a == 0:
			Alla.append(N)
		else:
			Alla.append(valuation(MyQp(a)))
	optionalprint(options, lambda: "The first 2k valuations of the a_j for " + str(p)+ ": " + str(Alla))
	# If the first k a_j are zero, then the sequence is the zero sequence. So, with high enough precision, this won't happen!
	for i in range(k):
		if Alla[i] == N:
			continue

		NewValuations = [Alla[j] - Alla[i] for j in range(i+1, i + mylrs.order)]
		mypower = 0
		
		while True in [a <= 0 for a in NewValuations]:
			mypower += 1
			NewValuations = [NewValuations[j] + j + 1 for j in range(mylrs.order - 1)]
		optionalprint(options, lambda: ("Jump:", L * p^mypower))
		return L* p^mypower
		# return (L * p^mypower, L, p, mypower)
	return 0





def splitsCompletely(f, p, N = 100):
	Fpt.<t> = FiniteField(p)[]
	for g in [h[0] for h in f.factor()]:
		if g.discriminant() % p == 0:
			return False
		else:
			if len(Fpt(g).roots()) != g.degree():
				return False
	return True

# This function assumes that u_0 = 0
# It searches for multiple primes p which each give rise to a m \ge 1 such that u_{mn} != for all n ge 1 
# Of course, the smallest possible m is returned
# So far, it only works on simple LRS

def stepComputeLRS(mylrs, options,  N = 20):
	# N is the accuracy of the p-adic computations
	
	initialgcd = gcd(mylrs.initial)
	mylrs = lrs(mylrs.order, [a/initialgcd for a in mylrs.initial], mylrs.recurrence)

	Z.<t> = ZZ[]

	# f is the characteristic polynomial of the LRS.
	f = Z(([1] + [-a for a in mylrs.recurrence])[::-1])

	# Compute a suitable prime p for the p-adic arithmatic
	AllPrimes = Primes()
	pp = AllPrimes.first()
	
	# This will save the best bound and the prime for which it is found
	MyBestBound = (0, 0)

	# These are the small primes from which the first estimates are computed
	MyPrimesAndBounds = []

	# Computing bounds for the initial set of primes.
	BoundForFirstStep = 3 * 2^mylrs.order

	# Extra step when some Bound is very low.
	MinLp = 0
	while pp < BoundForFirstStep or len(MyPrimesAndBounds) == 0:
		if mylrs.recurrence[-1] % pp != 0:
			Lp = ComputePeriod(f, pp)
			if pp == 2:
				Lp *= 2
			MyPrimesAndBounds.append((pp, Lp))
			if MinLp == 0 or Lp < MinLp:
				MinLp = Lp
			if pp > MinLp:
				break
		pp = AllPrimes.next(pp)

	# Compute steps for the primes with the best bounds. 
	# Loop is necessary if the step function fails at one point.
	MyPrimesAndBounds.sort(key=lambda tup: tup[1]) 
	ii = 0
	pTried = []
	while MyBestBound[0] == 0 and not ii >= len(MyPrimesAndBounds):
		p, Lp = MyPrimesAndBounds[ii][0], MyPrimesAndBounds[ii][1]
		if splitsCompletely(f, p, N):
			MyBestBound = (FindStepforSplittingp(mylrs, options, p), p)
		else:
			MyBestBound = (FindStepforSmallp(mylrs, options, p), p)
		pTried.append(p)
		optionalprint(options, lambda: "First attempt for the prime " + str(p) + " gave the step " + str(MyBestBound[0]))
		ii += 1



	# Compute whether any other small prime is likely to give a small bound. 
	for i in range(ii, len(MyPrimesAndBounds)):
		p, Lp = MyPrimesAndBounds[i][0], MyPrimesAndBounds[i][1]
		if Lp >= 2 * MyBestBound[0]:
			break
		if p in pTried: continue
		if splitsCompletely(f, p, N):
			StepForp = FindStepforSplittingp(mylrs, options, p, ToKill = True, KillBound = MyBestBound[0])
		else:
			StepForp = FindStepforSmallp(mylrs, options, p, ToKill = True, KillBound = MyBestBound[0])
		# print(p, StepForp)
		if StepForp < MyBestBound[0] and StepForp != 0:
			optionalprint(options, lambda: "Better step found with prime " + str(p) + " is " + str(StepForp))
			MyBestBound = (StepForp, p)
		
	# Compute if any other prime gives an even better step
	BoundForSecondStep = 2 * MyBestBound[0]
	while pp < BoundForSecondStep:

		if mylrs.recurrence[-1] % pp != 0 and ComputePeriod(f, pp) < BoundForSecondStep:
			if splitsCompletely(f, p, N):
				StepForp = FindStepforSplittingp(mylrs, options, pp, ToKill = True, KillBound = MyBestBound[0])
			else:
				StepForp = FindStepforSmallp(mylrs, options, pp, ToKill = True, KillBound = MyBestBound[0])

			if StepForp < MyBestBound[0] and StepForp != 0:
				optionalprint(options, lambda: "Better step found with prime " + str(pp) + " is " + str(StepForp))
				MyBestBound = (StepForp, pp)
				BoundForSecondStep = 2 * MyBestBound[0]

		pp = AllPrimes.next(pp)


	jump, p = MyBestBound
	reasoning = {
		"type" : "standard",
	}

	if MyBestBound[0] != 0:
		return jump, p, reasoning
	else:
		raise Exception("Something went wrong in the Step function!")


# This function assumes that u_0 = 0
# It searches for multiple primes p which each give rise to a m \ge 1 such that u_{mn} != for all n ge 1 
# It uses the fast algorithm that is not always successful nor does always return the 
# So far, it only works on simple LRS
def stepComputeLRSFast(mylrs, options):
	
	# divide by the gcd of initial values
	initialgcd = gcd(mylrs.initial)
	mylrs = lrs(mylrs.order, [a/initialgcd for a in mylrs.initial], mylrs.recurrence)

	Z.<t> = ZZ[]

	# f is the characteristic polynomial of the LRS.
	f = Z(([1] + [-a for a in mylrs.recurrence])[::-1])

	# Compute constant coefficient
	constantCoefficient = f(0)
	
	# Compute discriminant of char poly
	myDiscriminantPoly = f.discriminant()
	
	# Compute coincidence matrix
	myOrder = mylrs.order 
	valueList = mylrs.listn(2 * myOrder - 1)
	myCoincidenceMatrix = matrix([valueList[i : i + myOrder] for i in range(myOrder)])
	myDeterminantMatrix = myCoincidenceMatrix.determinant()
	# Compute a suitable prime p
	AllPrimes = Primes()
	pp = AllPrimes.first()
	
	# This will save the best bound and the prime for which it is found
	MyBestBound = (0, 0)

	# These are the small primes from which the first estimates are computed
	MyPrimesAndBounds = []
	
	# Computing bounds for the initial set of primes.
	BoundForFirstStep = 3 * 2^mylrs.order
	
	# Extra step when some bound is small.
	MinLp = 0
	while pp < BoundForFirstStep or len(MyPrimesAndBounds) == 0:
		if not (pp == 2 or constantCoefficient % pp == 0 or myDiscriminantPoly % pp == 0 or myDeterminantMatrix % pp == 0):
			Lp = ComputePeriod(f, pp)
			MyPrimesAndBounds.append((pp, Lp))
			optionalprint(options, lambda: (pp, Lp))
			if MinLp == 0 or Lp < MinLp:
				MinLp = Lp
			if pp > 2*MinLp and pp > 100:
				break
		pp = AllPrimes.next(pp)

	# Compute steps for the primes with the best bounds. 
	# Loop is necessary if the step function fails at one point.
	
	# Sort to try the smallest possible periods first
	MyPrimesAndBounds.sort(key=lambda tup: tup[1])

	# Only attempt the first 10 primes. If they fail, the method most likely does not apply
	MyPrimesAndBounds = MyPrimesAndBounds[:10]
	
	for primeAndBound in MyPrimesAndBounds:
		pp, periodModp = primeAndBound
		
		# The upper bound is almost always correct. To save time, we will not iterate it explicitly. 
		# Consider switching to mylrs.getPos (need to test)
		modpSquared = mylrs.listn(periodModp+1, modulo = pp^2)[periodModp]
		if modpSquared != 0:
			optionalprint(options, lambda: "Step found with prime " + str(pp) + " is " + str(periodModp))
			return(periodModp, pp, {
				"type" : "fast",
				"reason": "Step found with prime " + str(pp) + " is " + str(periodModp)
				})


	raise Exception("Something went wrong in the fast step function!")