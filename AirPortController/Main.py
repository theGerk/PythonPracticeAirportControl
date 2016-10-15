import AirportController
import TestData


for test in TestData.q:
	for lanes in range(10):
		airport = AirportController.AirportController(test, lanes + 1)
		while not airport.isComplete:
			if airport.tick():
				print airport.toString()
		print '-----------------------------------------------------\n'
