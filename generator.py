import sys
import argparse

parser = argparse.ArgumentParser(
                    prog='sage generator.py',
                    description='Generates random LRS')
parser.add_argument('filename', help="Output filename")
parser.add_argument('number',type=int, help="number of LRS to generate")
parser.add_argument('-t', '--type',default='csv', help="Output type (csv or tpls)")
parser.add_argument('-o', '--order',default=3,type=int, help="Order of LRS to generate, defaults to 3")
parser.add_argument('-b', '--bound',default=20,type=int, help="Maximum bound on the initial values and recurrence, defaults to 20")


args = parser.parse_args()
print(args.filename, args.number, args.type)


def getRandomLRS(order, recurrencebound = 20, initialbound = 20):
	""" Random LRS generator
	"""

	if recurrencebound == 0:
		raise Exception("can't have recurrencebound  = 0")

	recurrence = []
	initial = []
	for i in range(order-1):
		recurrence.append(random.randint(-recurrencebound, recurrencebound))
		initial.append(random.randint(-initialbound, initialbound))
	initial.append(random.randint(-initialbound, initialbound))

	while True:
		lastRecurrenceValue = random.randint(-recurrencebound, recurrencebound)

		if lastRecurrenceValue != 0:
			recurrence.append(lastRecurrenceValue)
			break

	return lrs.lrs(order, initial, recurrence)



with open(args.filename,"a") as f:

	if args.type == "csv":
		import csv
		cs = csv.writer(f)

	for i in range(args.number):

		lrs = getRandomLRS(args.order, args.bound, args.bound)


		if args.type == "csv":
			cs.writerow([lrs.order, " ".join([str(x) for x in lrs.recurrence]), " ".join([str(x) for x in lrs.initial])])
		elif args.type == "tpls":
			tpl = (lrs.order, tuple(lrs.recurrence), tuple(lrs.initial))
			f.write(str(tpl) + "\n")


