"""
The file to be run for this program.
"""

import AirportController
import sys


myFile = sys.stdin			#default file is stdin
lanes = 1					#default number of lanes is 1

#logic if one argument is passed
if len(sys.argv) == 2:
	try:	#first try and see if it's a valid number of lanes
		lanes = int(sys.argv[1])
		if lanes <= 0:
			raise ValueError('input out of range')
	except ValueError:	#if it isn't a valid number try and see if it's a file.
		try:
			myFile = open(sys.argv[1])
		except IOError:	#if it isn't a valid file then just tell the user it didn't work and use the defaults.
			print '"%s" is not a file or a valid integer' % sys.argv[1]
			print


#logic for 2 arguments passed in
elif len(sys.argv) == 3:
	#start by saying both myFile and lanes are uninizalized
	myFile = None
	lanes = None

	for arg in sys.argv[1:]:
		if lanes is None:
			#if lanes is uninizalized then try and see if this argument is a valid number of lanes
			try:
				lanes = int(arg)
				continue	#skips the file part if it's a valid number of lanes
			except ValueError:
				pass
		if myFile is None:
			#if input file is uninizalized then try and see if this argument is a valid file name
			try:
				myFile = open(arg, 'r')
				continue	#technically completley useles but it gives nice symetry with the other if statement
			except IOError:
				pass

	#if either the file or lanes are still unset, output to user so they know and set them back to defaults
	if myFile is None:
		print 'There is not a valid file input'
		myFile = sys.stdin
	if lanes is None:
		print 'There is not a valid integer input'
		lanes = 1


#initialize ariport controller
airport = AirportController.AirportController(myFile.readlines(), lanes)

#file is no longer used, so if it isn't stdin then close it.
if myFile != sys.stdin:
	myFile.close()


while not airport.isComplete:		#	isComplete checks if nothing new will ever happen when ticking through it.
	if airport.tick():				#	tick makes a tick happen... returns true if anything changed
		print airport.toString()	#	to string makes a string of all information there is needed about airport


