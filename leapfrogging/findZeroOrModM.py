import queue
from .resulttree import ResultTree
from . import stepcompute
import math
from utils.tuplestorage import TupleStorage 
from utils.linearset import LinearSet
from utils import subsequences
from utils.lrs import lrs
import time
from utils.helper import optionalprint
from utils.helper import gcdlist
from math import gcd

## Implements the main semi-algorithms of the skolem tool.


def moduloChecker(mylrs, modulo):
	# returns whether it is non-zero periodic modulo modulo
	# low memory implementation
	# must be periodic, not eventually periodic

	first = mylrs.listn(mylrs.order,modulo)

	# once we see the first values again we can stop and we have periodic behaviour
	searching = TupleStorage(first)

	if 0 in first:
		# print("\tSkipping... found initial zero " , first.index(0))
		return (False, "Zero", first.index(0), None)


	u = TupleStorage(first)
	i = mylrs.order - 1
	period = 0
	while True:
		i+=1
		period +=1
		nxt = mylrs.nextTupleStorage(u,modulo)
		if nxt == 0:
			# print("\tSkipping... found zero ", i)
			return (False, "Zero", i, None)
		if u.equals(searching):
			# print("\tStopping.... non-zero modulo", modulo)
			return (True, "ModuloPeriodic", modulo, period)

def interTwinedPeriodAlgorithm(mylrs, resultTree, options):
   
	# Divide initial values by their greatest common divisor
	if options.get('reducelrs'):
		mynewlrs = mylrs.getReducedLrs()
	else: 
		mynewlrs = mylrs
	
	resultTree.actualLrs = mynewlrs


	reverseLRS = mynewlrs.getShiftedNormalisedReverseLRS()
	#first elements
	firstF = mynewlrs.listn(mynewlrs.order)
	firstR = reverseLRS.listn(mynewlrs.order)

	#check if there are zeros in the first entries
	for i,x in enumerate(firstF):
		if x == 0:
			resultTree.setTypeZero(i)
			return
	for i,x in enumerate(firstR):
		if x == 0:
			resultTree.setTypeZero(-i)
			return

	# no, so we check in the remainder. 
	# TupleStorage = efficient storage of only order last values, without shifts inside a list
	uF = TupleStorage(firstF)
	uR = TupleStorage(firstR)

	# have done up to here
	i = mynewlrs.order - 1

	# period to check
	p = 1

	# constant coefficient of characteristic polynomial
	# any period to prove non-zeroness shold be coprime with this number
	constantCoefficient = mynewlrs.lastTerm()

	# by Skolems Conjecture, will terminate by zero or by mod m argument
	while True:

		if options.get('terminate') and options.get('terminate') < p:
			raise Exception("Cannot go that far") 

		optionalprint(options, lambda: ("still searching","period:", p))


		# next order(lrs) positions
		for ii in range(mylrs.order + 1):
			i += 1
			nxtF = mynewlrs.nextTupleStorage(uF)
			nxtR = reverseLRS.nextTupleStorage(uR)
			if nxtF ==0 :
				resultTree.setTypeZero(i)
				return
			if nxtR ==0 :
				resultTree.setTypeZero(-i)
				return
				
			firstF.append(nxtF)


		# Compute differences for all p subsequences
		differences = []
		for j in range(p):
			differences += [firstF[j+ii*p] - firstF[j+(ii+1)*p] for ii in range(mylrs.order)]
			
		G = abs(gcdlist(differences))

		if G == 0:
			# This should only occur when the LRS is constant
			G = abs(firstF[0]) + 1
			if G == 1:
				# We are somehow dealing with the zero LRS here
				raise Exception("Input zero sequence?")

		# Deal with banned moduli 
		while abs(gcd(G, int(mynewlrs.lastTerm()))) > 1:
			G = abs(int(G / gcd(G, mynewlrs.lastTerm())))
		
		if True not in [x % G == 0 for x in firstF]:
			optionalprint(options, lambda: ("ModuloPeriodic", p, abs(G)))
			resultTree.setTypeModM(G, p)
			return
		else:
	 		p+=1



def interTwinedModuloAlgorithm(mylrs,resultTree,options):

	# Divide initial values by their greatest common divisor
	if options.get('reducelrs'):
		mynewlrs = mylrs.getReducedLrs()
	else: 
		mynewlrs = mylrs

	resultTree.actualLrs = mynewlrs


	reverseLRS = mynewlrs.getShiftedNormalisedReverseLRS()
	#first elements
	firstF = mynewlrs.listn(mynewlrs.order)
	firstR = reverseLRS.listn(mynewlrs.order)

	#check if there are zeros in the first entries
	for i,x in enumerate(firstF):
		if x == 0:
			resultTree.setTypeZero(i)
			return

	for i,x in enumerate(firstR):
		if x == 0:
			resultTree.setTypeZero(-i)
			return

	#no, so we check in the remainder. 
	# TupleStorage = efficient storage of only order last values, without shifts inside a list
	uF = TupleStorage(firstF)
	uR = TupleStorage(firstR)

	# last checked index 
	i = mynewlrs.order - 1

	# Find modm set up
	modulo = 1
	
	gaptime = 100000
	switches = -1
	while True:

		if gaptime < 1000000000:
			gaptime = gaptime * 2

		switches +=1

		if (switches & (switches-1) == 0) and switches > 10:
			optionalprint(options,lambda: ("#switches is", switches))
			pass
         
        # spend some time on mod m
		starttime = time.time_ns()
		while time.time_ns() - starttime < gaptime: 
			# note we start at 2
			modulo += 1

			if (modulo & (modulo-1) == 0) and modulo > 10:
				optionalprint(options,lambda: ("Still searching for modulo at", modulo))
				pass

			# skip bad modulos
			if math.gcd(modulo, mynewlrs.lastTerm()) != 1:
				continue

			# return if proven non-zero
			(result, typ, place, period) = moduloChecker(mynewlrs, modulo)
			optionalprint(options, lambda: ("modulochecker result", result, typ, place, period))
			if result:
				resultTree.setTypeModM(modulo, period)
				return

		# spend some time on find zero
		starttime = time.time_ns()
		while time.time_ns() - starttime < gaptime: 
			# index to check now!
			i+=1
			nxtF = mynewlrs.nextTupleStorage(uF)
			nxtR = reverseLRS.nextTupleStorage(uR)
			if nxtF ==0 :
				resultTree.setTypeZero(i)
				return
			if nxtR ==0 :
				resultTree.setTypeZero(-i)
				return

			# just a message to make it clear that it is still doing something
			# outputs if i = 2^k for some k
			if (i & (i-1) == 0) and i > 10:
				optionalprint(options,lambda: ("Still searching for zero at", i))
				pass

def interTwinedAlgorithm(mylrs,resultTree,options):
	     
	if not options.get("smallestm"):
		return interTwinedPeriodAlgorithm(mylrs,resultTree,options)
	else:
		return interTwinedModuloAlgorithm(mylrs,resultTree,options)

def getSufficientJump(mylrs, zeroIndex, options):
	# input the lrs and the location of a zero in that lrs
	# return sufficient jump so that u_{zeroIndex + jump*N} has no further zeros.

	#forward
	if zeroIndex >=0:
		shifted = mylrs.shift(zeroIndex)
		
	#very backwards
	elif zeroIndex <= -mylrs.order+1:

		nsrLRS = mylrs.getShiftedNormalisedReverseLRS()
		first = nsrLRS.listn(-zeroIndex+1)[-mylrs.order:]
		normalisedInitial = [y*mylrs.lastTerm()**i for i,y in enumerate(reversed(first))]
		shifted = lrs(mylrs.order, normalisedInitial, mylrs.recurrence) 
	else:
		#  -mylrs.order+1 < zeroIndex < 0:
		# straddles both sides of 0
		nsrLRS = mylrs.getShiftedNormalisedReverseLRS()
		first = nsrLRS.listn(-zeroIndex+1)[-mylrs.order:]
		normalisedInitialp1 = [y*mylrs.lastTerm()**i for i,y in enumerate(reversed(first))]
		second = mylrs.listn(mylrs.order + zeroIndex)[1:]
		normalisedInitialp2 = [y*mylrs.lastTerm()**(-zeroIndex) for y in second]
		shifted = lrs(mylrs.order, normalisedInitialp1 + normalisedInitialp2, mylrs.recurrence) 

	if options.get("usefastjump"):
		try:
			return stepcompute.stepComputeLRSFast(shifted, options)
		except:
			return stepcompute.stepComputeLRS(shifted, options)
	else:
		return stepcompute.stepComputeLRS(shifted, options)


def findZeroOrModM(mylrs, resultTree, options):
	

	interTwinedAlgorithm(mylrs,resultTree,options)


	if resultTree.isZero():
		# this lrs has a zero at zeroIndex
		zeroIndex = resultTree.zero

		# compute the sufficient jump
		sufficientJump,p,reasoning = getSufficientJump(mylrs, zeroIndex, options)
		
		resultTree.zeroAddJumpInfo(sufficientJump,p, reasoning)


		if options.get('mergesubcases'):
			factorJump = subsequences.factorIntoSteps(sufficientJump)
		else:
			factorJump = [(sufficientJump, list(range(1,sufficientJump)))]

		currentLS = LinearSet(zeroIndex, sufficientJump)
		nextResultTree = ResultTree(None, currentLS.mapInside(resultTree.linearOfFullSet), currentLS)
		nextResultTree.setTypePAdicNonZero(zeroIndex, sufficientJump, p)
		resultTree.addChild(nextResultTree)	

		for currentJump, offsets in factorJump:


			# common recurrence to the subsequences
			firstMany = mylrs.listn(currentJump*mylrs.order)
			cpm = subsequences.getCompanionMatrix(mylrs)
			cpmp = subsequences.powermatrix(cpm, currentJump)
			recurrence = subsequences.getRecurrence(cpmp)


			# compute the correct offsets and recurse
			for i in offsets:
				currentLS = LinearSet((zeroIndex + i) % currentJump, currentJump)
				initital = subsequences.getInitial(firstMany, currentLS, mylrs.order)
				nextmyLRS = lrs(mylrs.order, initital, recurrence)
				# print(nextmyLRS)

				nextResultTree = ResultTree(nextmyLRS, currentLS.mapInside(resultTree.linearOfFullSet), currentLS)
				resultTree.addChild(nextResultTree)
				# get the results of the recurrence, then map them back into the indices they came from.
				findZeroOrModM(nextmyLRS, nextResultTree,options)


	else: #isModM
		#already dealt with inside interTwinedAlgorithm
		pass



