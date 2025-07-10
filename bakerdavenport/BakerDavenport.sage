from utils.lrs import *
from utils.subsequences import charpolylrs, isDegenerate

# Assume that f(0) < 0, lim_{n -> infty} f(n) > 0 and f is monotonically increasing. 
# This function searches for positive integers k such that f(k) > 0 and f(k-1) <= 0
def findPositiveRoot(f):
	k = 1
	while f(k) < 1:
		k *= 2
	if k < 3:
		return k
	step = k // 4
	while step > 0.8:
		kNew = k - step
		if f(kNew) > 1:
			k = kNew
		step //= 2
	return k


# Returns the distance of a real number to the nearest integer
def ratPart(a):
	return abs(round(a) - a)


# Given a bound and a LRS, returns a list of likely zeroes.
def localArgument(mylrs, bound):
	# if a in left, then u_n can only be zero if n = a mod step
	step, left = 1, [0]

	allPrimes = Primes()
	p = allPrimes.first()

	# Only use primes coprime to a_k!
	forbiddenCoeff = mylrs.recurrence[-1]

	# Remove all double factors and factors of degree 1. These don't matter to find Chebotarev primes
	f = charpolylrs(mylrs)
	newf = 1
	for fact in factor(f):
		if fact[0].degree() > 1:
			newf *= fact[0]
	f = newf

	# Arbitrary bound, might need to be tweaked
	while step < 10^6 * bound:
		Zp.<t> = FiniteField(p)[]
		fp = Zp(f)
		if len(factor(fp)) == f.degree() and forbiddenCoeff % p != 0:
			modpList = mylrs.getRepitionModuloList(p)[:-mylrs.order]

			# periodModulop is the period of the LRS modulo p. As periods are most likely not coprime, we can eliminate a lot of numbers.
			periodModulop = len(modpList)
			overlap = gcd(periodModulop, step)
			zeroIndex = [i for i in range(len(modpList)) if modpList[i] == 0]
			newLeft = []

			# Combine the zeroes of the previous primes and this prime using the Chinese remainder theorem (crt)
			for i in zeroIndex:
				for j in left:
					if (i-j) % overlap == 0:
						newCrt = crt([i, j], [periodModulop, step])
						if not newCrt in newLeft:
							newLeft.append(newCrt)
			left = sorted([a for a in newLeft if a < bound])
			step *= periodModulop / overlap
		p = allPrimes.next(p)

	# We return the bound of the largest possible zero. If we eliminated everything, return the 0 as a bound.
	if len(left) == 0:
		return [0]
	return left


# Identifies rational numbers with continued fractions. Make sure the denominator is smaller than 2^200
def identifyRationalDenominator(q, precision):
	newContFrac = []
	for i in list(QQ(q.real()).continued_fraction()):
		if i < 2^(precision / 2):
			newContFrac.append(i)
		else:
			break
	return continued_fraction(newContFrac).value().denominator()


# Computes the height of an algebraic number given a list of cunjugates (as complex numbers)
def heightCoeffList(coeffsList, precision, polRing):
	C = ComplexField(precision)
	Ct.<tt> = C[]
	
	# Compute the minimal polynomial over the real numbers and the first part of the height formula
	minPol, MySum = 1, 0
	for coeff in coeffsList:
		minPol *= tt - coeff
		MySum += log( max( 1, abs(coeff) ) )
	
	minPolList = [coeff.real() for coeff in list(minPol)]

	# Identify the coefficients of the polynomial as rational numbers and multiply by a number to make them all integers.
	denominatorNeeded = lcm([identifyRationalDenominator(a, precision) for a in minPolList])

	# minPolRat is the minimum polynomial with its identified rational coefficients.
	minPolRat = polRing([int(round(coeff.real())) for coeff in list(minPol * denominatorNeeded)])

	MySum += log(abs(C(minPolRat.leading_coefficient())))

	return C(MySum / len(coeffsList))


# Estimate the height of the quotient of two roots of a polynomial
def heightPolQuotient(coeffListList, precision, polRing):
	heights = [heightCoeffList(coeffList, precision, polRing) for coeffList in coeffListList]
	d = len(heights) - 1
	return sum(heights) + d * log(2), (d * (d + 1)) / 2


def heightList(List, precision):
	mySum = 0
	for root in List:
		mySum += max(0, log(abs(root)))
	return mySum / len(List)


# Computes a bound if there is exactly one dominant root
def boundFor1DominantRoot(domRoot, coeffsDom, upperBoundCoeffLow, biggestNonDomRoot):
	
	# We will just take the naive approach and bound using numerical methods.
	coeffsDom = [abs(coeff/upperBoundCoeffLow) for coeff in coeffsDom]
	leadingCoeff, lowerCoeff, power = coeffsDom[-1], sum(coeffsDom[:-1]), len(coeffsDom) - 1
	newDomRoot = domRoot / biggestNonDomRoot
	if power == 0:
		def f(n):
			return leadingCoeff * newDomRoot**n - 1
	else:
		def f(n):
			return (leadingCoeff * n - lowerCoeff ) * newDomRoot**n * n**(power-1) - 1
	return True, findPositiveRoot(f)



def boundFor2or3DominantRoots(mylrs, domCoeff2, allCoeff, polyDom2, infoThirdRoot, upperBoundCoeff, biggestNonDomRoot, precision):
	
	# Unpack the third root if necessary
	has3DomRoots = infoThirdRoot[0]
	if has3DomRoots:
		domCoeff3, polyDom3 = infoThirdRoot[1], infoThirdRoot[2]

	
	R = RealField(precision)
	precisionBound = R(2)^(-precision + 50)
	bounds = []
	
	# Compute lambda, alpha
	largestRootAbs = max([R(abs(myTuple[0])) for myTuple in domCoeff2])
	indexOfLambda = [i for i in range(len(domCoeff2)) if largestRootAbs - R(abs(domCoeff2[i][0])) < precisionBound][0]
	lamda, alpha = domCoeff2[indexOfLambda][0], domCoeff2[indexOfLambda][1][0]
	lambdaP, alphaP = lamda/abs(lamda), alpha/abs(alpha)


	# Scale the biggest non-dominant root
	print(charpolylrs(mylrs))
	biggestNonDomRoot = biggestNonDomRoot / abs(lamda)

	# Compute rho, b
	if has3DomRoots:
		indexOfRho = [i for i in range(len(domCoeff3)) if largestRootAbs - R(abs(domCoeff3[i][0])) < precisionBound][0]
		rho, bP = domCoeff3[indexOfRho][0], R(domCoeff3[indexOfRho][1][0].real())/R(abs(alpha))
		if rho < 0:
			lambdaP *= -1	
	
	# Scale the remaining roots

	# If the real root has has a higher multiplicity or an equal multiplicity and a high coefficient, a far cheaper estimate can be made.
	if has3DomRoots and bP > 2*alpha + precisionBound:

		domCoeff2, domCoeff3 = [2*abs(a) for a in domCoeff2[indexOfLambda][1]], [abs(a) for a in domCoeff3[indexOfRho][1]]
		lead, sec = domCoeff2[-1] -  domCoeff3[-1], sum(domCoeff2[:-1]) + sum(domCoeff3[:-1])
		
		# Solve lead - sec / n - upperBoundCoeff * biggestNonDomRoot^n > 0
		def f(n):
			return biggestNonDomRoot^-n - n
		bounds.append(findPositiveRoot(f))
		print(bounds[0],ComplexField()(biggestNonDomRoot^-1))
		bounds.append(int((sec + upperBoundCoeff)/lead) + 1)
		print("Easy case, bound is n <= ", max(bounds))
		return True, max(bounds)


	# Computing the degree of the extension is (relatively) expensive. 
	# Hence, use that the degree is bounded by the factorial of the degree.
	degreeExt = R(factorial(polyDom2.degree()))
	if has3DomRoots:
		degreeExt *= 8 * factorial(polyDom3.degree())
	else:
		degreeExt *= 4
	

	# Next, we compute an upper bound for h(lambda) and hP(lambdaP)
	hlambda = heightList([R(abs(coeff[0])) for coeff in domCoeff2], precision)
	hPlambdaP = max(2 * hlambda, R(pi))

	# Compute a bound for h(alpha)
	conjAlpha = [coeff[1][0] for coeff in domCoeff2]
	halpha = heightCoeffList(conjAlpha, precision, polyDom2.parent())

	# Compute an upper bound for h(b)
	if has3DomRoots:
		conjb = [R(coeff[1][0].real()) for coeff in domCoeff3]
		hb = heightCoeffList(conjb, precision, polyDom2.parent())

	# Compute an upper bound for hPgamma
	if has3DomRoots:
		hPgamma = max(4*R(log(2)) + 4*halpha + 4*hb, R(pi))
	else:
		hPgamma = max(2*halpha, R(pi))

	MatveevConstant = -30^6 * 3^6.5 * degreeExt^2 * (1 + log(R(degreeExt))) * hPlambdaP * hPgamma

	
	# Solve MatveevConstant * (1 + log(2n)) < log(upperBoundCoeff/2) + n * log(biggestNonDomRoot)

	def f(n):
		return R(-log(upperBoundCoeff/2) - n * log(biggestNonDomRoot) + MatveevConstant * (1 + log(2*n)))

	uglyBound = findPositiveRoot(f)
	
	print("Large bound found by Baker: n <= ", uglyBound)

	if has3DomRoots:
		gammaList = (2*alphaP/(-bP + sqrt(bP^2 - 4)), 2*alphaP/(-bP - sqrt(bP^2 - 4)))
	else:
		gammaList = (alphaP, -alphaP)

	combinationsToCheck = []
	for gamma in gammaList:
		combinationsToCheck += [(gamma, lambdaP), (-gamma, -lambdaP)]


	for tupleToCheck in combinationsToCheck:
		gamma, lambdaP = tupleToCheck
		argumentLambda = QQ(R(arg(lambdaP)/pi)).continued_fraction()
		Denominators = [a.denominator() for a in argumentLambda.convergents()]
		A = upperBoundCoeff / 2
		B = biggestNonDomRoot^-1
		kappa = R(arg(lamda)/pi)
		mu = R(arg(gamma)/pi - 1/2)
		M = uglyBound
		possibleBound = []
		for Q in Denominators:
			if Q <= 6 * M: 
				continue
			epsilon = ratPart(mu * Q) - M * ratPart(kappa * Q)
			if epsilon <= 0: 
				continue
			possibleBound.append(Q/epsilon)
			if len(possibleBound) >= 5:
				break
		if len(possibleBound) < 1:
			print("Something went wrong. The Baker-Davenport reduction method does not seem to apply")
			print("A slightly slower method will be used")
			bounds.append(max(localArgument(mylrs, M)) + 1)
		else:	
			bounds.append(int(R(log(A * min(possibleBound))/log(B))) + 1)
	return True, max(bounds)



# Returns the largest N such that u_N can be zero using a Baker-style argument
# This function does not check non-degeneracy
# The LRS is assumed to be non-degenerate and non-constant
def findDominantRoots(mylrs):
	
	precision = 1000
	C = ComplexField(precision)
	PrecisionBound = C(2)^(-precision + 50)
	Cx.<x> = C[]
	QQt.<t> = QQbar[]

	# Characteristic polynomial of the LRS
	poly = charpolylrs(mylrs)

	# Factoring the characteristic polynomial
	polyFactored = poly.factor()

	# Splitting Fators and their multiplicity
	polyFactors, polyMult = [fact[0] for fact in polyFactored], [fact[1] for fact in polyFactored]

	# Compute roots in the complex number and search for all dominant roots
	myRoots = [[root[0] for root in QQt(fact).roots()] for fact in polyFactors]
	rootsAbs = [[abs(root).real() for root in fact] for fact in myRoots]
	
	# We use some approximation here
	BiggestRoot = 0
	for roots in rootsAbs:
		for root in roots:
			if C(BiggestRoot) - C(root) < PrecisionBound:
				BiggestRoot = C(root)
	
	FactorsWithBigRoots = [[root for root in roots if abs(BiggestRoot - C(root)) < PrecisionBound] for roots in rootsAbs]
	
	NumberOfDominantRoots = sum([len(roots) for roots in FactorsWithBigRoots])

	domPols = [polyFactors[i] for i in range(len(polyFactors)) if len(FactorsWithBigRoots[i]) > 0]
	

	# We had an approximation. Using resultants, we can check whether they are truly different
	# If so, the algorithm should be run at higher precision, but as this case is very rare, we have not implemented it
	if len(domPols) > 1:
		QQt2.<t2> = QQt[]
		resultantsGCD = gcd([poly(t2).resultant(QQt2(t2^poly.degree() * poly(t/t2))) for poly in domPols])
		if resultantsGCD.degree() < 1: 
			print("Dominant roots too close together ")
			raise ValueError("Dominant roots too close together ")
			return False, 0 

	# Check whether Baker can be applied
	# If there are more than 3 dominant roots, we cannot apply our method
	if NumberOfDominantRoots > 3:
		print("Too many dominant roots to apply the Baker theorem ")
		raise ValueError("Too many dominant roots to apply the Baker theorem ")
		return False, 0

	# Create VanDerMonde matrix with the characteristic roots (including multiplicity)
	myMatrix, allRoots = [], []
	for i in range(len(polyFactors)):
		for root in myRoots[i]:
			allRoots.append((root, polyMult[i]))
			for j in range(polyMult[i]):
				myMatrix.append([k^j * C(root)^k for k in range(mylrs.order)])
	
	# Compute coefficients of the exponential polynomial
	# The coefficients will be saved as complex floats as doing these computations with algebraic numbers is too slow
	coeffExponentialPolynomial = list(matrix(myMatrix).transpose().inverse() * vector(mylrs.initial))


	# allcoeff saves the coefficients of the exp-poly form, c is a counter,
	# upperBoundCoeff * (n^maxLowMult) * biggestNonDomRoot^n grows faster than the non-dominant part of the LRS.
	allCoeff, c, maxLowMult, upperBoundCoeff, biggestNonDomRoot = [], 0, 0, 0, 0
	domCoeff = [[] for i in range(len(domPols))]

	for rootTuple in allRoots:
		coeffForRoot = []
		for i in range(rootTuple[1]):
			coeffForRoot.append(coeffExponentialPolynomial[c])
			c += 1
		absroot = abs(C(rootTuple[0]))
		# Bound the size of non-dominant roots
		if abs(absroot - BiggestRoot) > PrecisionBound:
			upperBoundCoeff += sum([abs(coeff) for coeff in coeffForRoot])

			maxLowMult = max( len(coeffForRoot), maxLowMult)
			
			# Doing this part with algebraic numbers is very slow for some reason
			if absroot > biggestNonDomRoot and not abs(C(absroot) - C(biggestNonDomRoot)) < PrecisionBound: 
				biggestNonDomRoot = absroot

		for i in range(len(domPols)):
			if domPols[i](rootTuple[0]) == 0:
				domCoeff[i].append((rootTuple[0], coeffForRoot))
		allCoeff.append((rootTuple[0], coeffForRoot))

	if True in [abs(coeff[1][-1]) < PrecisionBound for coeff in allCoeff]:
		# This LRS has zero coefficients and is not minimal
		print("LRS has zero coefficients")
		raise ValueError("LRS has zero coefficients")
		return False, 0

	# The case that all roots are dominant. Add a very small root to avoid adding annoying subcases
	if upperBoundCoeff == 0:
		upperBoundCoeff, biggestNonDomRoot, maxLowMult = 1/10000, 1/10000, 1

	# If the non-dominant part is non-simple, make it simple by increasing the non-dominant root.
	if maxLowMult != 1:
		# If the non-dominant part is not simple, we estimate it with a slightly bigger root. 
		# Only, this holds only for n >= bound1, which we need to compute

		power = maxLowMult - 1
		newmaxdomroot = max([max([abs(myTuple[0]) for myTuple in domCoeffOnePoly]) for domCoeffOnePoly in domCoeff])

		newBiggestNonDomRoot = sqrt(newmaxdomroot * biggestNonDomRoot)
		def f(n):
			return newBiggestNonDomRoot^n - n^power * biggestNonDomRoot^n
		bound1 = findPositiveRoot(f)
	else:	# If the non-dominant part is simple, do nothing
		newBiggestNonDomRoot = biggestNonDomRoot
		bound1 = 0
	
	print("Number of dominant roots", NumberOfDominantRoots)

	if NumberOfDominantRoots == 1:
		# Exactly one dominant root. We only need the coefficients in front of it, not its Galois conjugates.

		domCoeff = domCoeff[0]
		domrootindex = [myTuple for myTuple in domCoeff if BiggestRoot - abs(myTuple[0]) < PrecisionBound][0]  
		domRoot, coeffs = abs(domrootindex[0]), domrootindex[1]
		success, bound = boundFor1DominantRoot(domRoot, coeffs, upperBoundCoeff, newBiggestNonDomRoot)
	else: # General case

		domPol2 = [polyFactors[i] for i in range(len(polyFactors)) if len(FactorsWithBigRoots[i]) == 2][0]

		if NumberOfDominantRoots == 2:
			infoThirdRoot = (False,)
			domCoeff2 = domCoeff[0]
		else:
			domPol3 = [polyFactors[i] for i in range(len(polyFactors)) if len(FactorsWithBigRoots[i]) == 1][0]
			if len(domCoeff[0]) == 2:
				domCoeff2, domCoeff3 = domCoeff[0], domCoeff[1]
			else:
				domCoeff2, domCoeff3 = domCoeff[1], domCoeff[0]
			
			infoThirdRoot = (True, domCoeff3, domPol3)

		success, bound = boundFor2or3DominantRoots(mylrs, domCoeff2, allCoeff, domPol2, infoThirdRoot, upperBoundCoeff, newBiggestNonDomRoot, precision)
	
	return success, max(bound, bound1)