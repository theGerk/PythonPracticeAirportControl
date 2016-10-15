import AirportController
import TestData


for test in TestData.q:
		lanes = 0
		airport = AirportController.AirportController(test, lanes + 1)
		while not airport.complete:
			if airport.tick():
				print airport.toString()
		print '\n-----------------------------------------------------\n'
