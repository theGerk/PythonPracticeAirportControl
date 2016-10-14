import PriorityQueue

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


class AirPortController:
	def __init__(self, airplaneRequests):
		self.__airplaneRequests = airplaneRequests
		self.__currentIndexInAirplaneRequests = 0
		self.__queue = PriorityQueue.PriorityQueue(CreateComparetor([(2, False), (1, False), (3, False)], False))
		self.__currentTime = -1
		self.__currentPlane = None # (end time, request)

		self.__complete()


	def __tick(self):
		self.__currentTime += 1

		#move plane out of runway if it is in it
		if self.__currentPlane is not None and self.__currentPlane[0] == self.__currentTime:
			self.__currentPlane = None

		while self.__currentIndexInAirplaneRequests < len(self.__airplaneRequests):
			airplane = self.__airplaneRequests[self.__currentIndexInAirplaneRequests]
			if airplane[1] == self.__currentTime:
				self.__queue.insert(airplane)
			else:
				break
			self.__currentIndexInAirplaneRequests += 1

		peek = self.__queue.peek
		if self.__currentPlane is None and peek is not None and peek[2] <= self.__currentTime:
			tmp = self.__queue.take()
			self.__currentPlane = (tmp[3] + self.__currentTime, tmp)

		print self.toString()


	def __complete(self):
		while self.__currentIndexInAirplaneRequests < len(self.__airplaneRequests) or not self.__queue.isEmpty or self.__currentPlane is not None:
			self.__tick()


	def toString(self):
		if self.__currentPlane is None:
			s = 'there is no plane on the runway.'
		else:
			s = '{0} is currently on the runway and will take off in {1} ticks.'.format(self.__currentPlane[1][0], self.__currentPlane[0] - self.__currentTime)
		output = 'The time is currently t = {0} and {1}\n'.format(self.__currentTime, s) + 'The request queue:\n'
		formatString = '{0}: Request submitted at t = {1} for t = {2}. Will take {3} ticks to take off.\n'
		for entry in self.__queue.toArray():
			output += formatString.format(entry[0],entry[1],entry[2],entry[3])
		return output

import TestData
plane = AirPortController(TestData.q)