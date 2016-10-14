import PriorityQueue

lanes = 1

# argumentArray in form of tuples, with first entry being the index name, the second being a boolean
#                                                                                               True => greater gets precedence
#                                                                                               False => lesser gets precedence
def CreateComparetor(argumentArray, firstGetsPreference):
	def output(a, b, acumulator = None):
		for arg in argumentArray:
			if a[arg[0]] != b[arg[0]]:
				return (a[arg[0]] > b[arg[0]]) == arg[1]
		return firstGetsPreference
	return output


def isAllNone(input):
	for elem in input:
		if elem is not None:
			return False
	return True

class AirPortController: 
	def __init__(self, airplaneRequests):
		self.__airplaneRequests = airplaneRequests
		self.__currentIndexInAirplaneRequests = 0
		self.__queue = PriorityQueue.PriorityQueue(CreateComparetor([(2, False), (1, False), (3, False)], False))
		self.__currentTime = -1
		self.__currentPlanes = [None] * lanes # [(end time, request)]

		self.__complete()


	def __tick(self):
		self.__currentTime += 1

		#move planes out of runways if they are done taking off
		i = 0
		while i < len(self.__currentPlanes):
			if self.__currentPlanes[i] is not None and self.__currentPlanes[i][0] == self.__currentTime:
				self.__currentPlanes[i] = None
			i += 1

		#add new requests into queue
		while self.__currentIndexInAirplaneRequests < len(self.__airplaneRequests):
			airplane = self.__airplaneRequests[self.__currentIndexInAirplaneRequests]
			if airplane[1] == self.__currentTime:
				self.__queue.insert(airplane)
			else:
				break
			self.__currentIndexInAirplaneRequests += 1

		#move new planes into runway
		i = 0
		while i < len(self.__currentPlanes):
			peek = self.__queue.peek
			if self.__currentPlanes[i] is None and peek is not None and peek[2] <= self.__currentTime:
				tmp = self.__queue.take()
				self.__currentPlanes[i] = (tmp[3] + self.__currentTime, tmp)
			elif peek is None or peek[2] > self.__currentTime:
				break
			i += 1

		print self.toString()


	def __complete(self):
		while self.__currentIndexInAirplaneRequests < len(self.__airplaneRequests) or not self.__queue.isEmpty or not isAllNone(self.__currentPlanes):
			self.__tick()


	def toString(self):
		output = 'The time is currently t = {0}.\n'.format(self.__currentTime)
		output += 'The runways:\n'
		runwayFormatString = '\t{0} is currently on runway {2} and will take off in {1} ticks.\n'
		emptyRunwayFormatString = '\tRunway {0} is currently empty.\n'
		queueFormatString = '\t{0}: Request submitted at t = {1} for t = {2}. Will take {3} ticks to take off.\n'

		i = 0
		while i < len(self.__currentPlanes):
			plane = self.__currentPlanes[i]
			if plane is None:
				output += emptyRunwayFormatString.format(i)
			else:
				output += runwayFormatString.format(plane[1][0], plane[0] - self.__currentTime, i)
			i += 1

		output += 'The request queue:\n'

		for entry in self.__queue.toArray():
			output += queueFormatString.format(entry[0],entry[1],entry[2],entry[3])
		
		return output

import TestData
plane = AirPortController(TestData.q)