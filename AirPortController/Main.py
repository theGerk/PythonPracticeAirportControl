import AirportController
import TestData
import sys


def lineToRequst(line):
	a = line.split(',')
	return (a[0], int(a[1]), int(a[2]), int(a[3]))


myFile = sys.stdin
lanes = 1
if len(sys.argv) == 2:
	try:
		lanes = int(sys.argv[1])
		if lanes <= 0:
			raise ValueError('input out of range')
	except ValueError:
		try:
			myFile = open(sys.arg[1])
		except IOError:
			print '"%s" is not a file or a valid integer' % sys.argv[1]
			print
elif len(sys.argv) == 3:
	myFile = None
	lanes = None
	for arg in sys.argv[1:]:
		if lanes is None:
			try:
				lanes = int(arg)
				continue
			except ValueError:
				pass
		if myFile is None:
			try:
				myFile = open(arg, 'r')
				continue
			except IOError:
				pass

	if myFile is None:
		print 'There is not a valid file input'
		myFile = sys.stdin
	if lanes is None:
		print 'There is not a valid integer input'
		lanes = 1


airport = AirportController.AirportController([lineToRequst(line) for line in myFile.readlines()], lanes)
while not airport.isComplete:
	if airport.tick():
		print airport.toString()


