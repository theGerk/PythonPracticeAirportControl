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

	def tick(self):
		self.__currentTime += 1

		#move plane out of runway if it is in it
		if self.__currentPlane is not None and self.__currentPlane[0] == self.__currentTime:
			self.__currentPlane = None

		while self.__currentIndexInAirplaneRequests < len(self.__airplaneRequests):
			airplane = self.__airplaneRequests[self.__currentIndexInAirplaneRequests]
			if airplane[1] == self.__currentTime:
				self.__queue.insert(airplane)
			self.__currentIndexInAirplaneRequests += 1

		if self.__currentPlane is None and self.__queue.peek()[2] <= self.__currentTime:
			self.__currentPlane = self.__queue.take()

