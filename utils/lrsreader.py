from .lrs import lrs
import sys
import re

def lrsreader(lst):
	if len(lst) <2:
		raise ValueError("Incorrect number of lines in the input (2 required)")


	characterRegex = re.compile(r'[a-zA-Z]')
	if characterRegex.search(lst[0]) or characterRegex.search(lst[1]):
		raise ValueError("There shouldn't be any letters in the input")


	numberRegex = re.compile(r'-?\d+')
	second = [x for x in numberRegex.findall(lst[0].strip())]
	third = [x for x in numberRegex.findall(lst[1].strip())]

	order = len(second)
	if order<= 0:
		raise ValueError("Order must be at least 1")
	
	recurrence = [int(x) for x in second]

	if recurrence[-1] == 0:
		raise ValueError("Recurrence must have non-zero final value (otherwise the order can be reduced by 1)")

	initial = [int(x) for x in third]

	if len(recurrence) != len(initial):
		raise ValueError("The number of initial values does not match the order (the number of elements in the recurrence).")


	return lrs(order, initial, recurrence)


def readLRS(position=2):
	lines = []

	if len(sys.argv) > position:
		with open(sys.argv[position], 'r') as f:
			for line in f:
				lines.append(line)
	else:
		for i in range(2):
			lines.append(input())

	mylrs = lrsreader(lines)

	return mylrs

