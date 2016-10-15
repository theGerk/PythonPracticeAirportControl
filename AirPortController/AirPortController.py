import PriorityQueue


def isAllNone(input):
	for elem in input:
		if elem is not None:
			return False
	return True


def getFirstMinIndex(input):
	if not (len(input) > 0):
		return None
	minIndex = 0
	i = 1
	while i < len(input):
		if input[i] < input[minIndex]:
			minIndex = i
		i += 1
	return minIndex

def getFirstMaxIndex(input):
	if not (len(input) > 0):
		return None
	minIndex = 0
	i = 1
	while i < len(input):
		if input[i] > input[maxIndex]:
			maxIndex = i
		i += 1
	return maxIndex

class AirportController: 
	def __init__(self, airplaneRequests, lanes):
		self.__airplaneRequests = airplaneRequests
		self.__currentIndexInAirplaneRequests = 0
		self.__queue = PriorityQueue.PriorityQueue(PriorityQueue.CreateComparetor([(2, False), (1, False), (3, False)], False))
		self.__currentTime = -1
		self.__runways = [None] * lanes # [(end time, request)]


	def tick(self):
		self.__currentTime += 1
		changeDetected = False

		#move planes out of runways if they are done taking off
		i = 0
		while i < len(self.__runways):
			if self.__runways[i] is not None and self.__runways[i][0] == self.__currentTime:
				self.__runways[i] = None
				changeDetected = True
			i += 1

		#add new requests into queue
		while self.__currentIndexInAirplaneRequests < len(self.__airplaneRequests):
			airplane = self.__airplaneRequests[self.__currentIndexInAirplaneRequests]
			if airplane[1] == self.__currentTime:
				self.__queue.insert(airplane)
				changeDetected = True
			else:
				break
			self.__currentIndexInAirplaneRequests += 1

		#move new planes into runway
		i = 0
		while i < len(self.__runways):
			peek = self.__queue.peek
			if self.__runways[i] is None and peek is not None and peek[2] <= self.__currentTime:
				tmp = self.__queue.take()
				self.__runways[i] = (tmp[3] + self.__currentTime, tmp)
				changeDetected = True
			elif peek is None or peek[2] > self.__currentTime:
				break
			i += 1

		return changeDetected

	@property
	def complete(self):
		return self.__currentIndexInAirplaneRequests >= len(self.__airplaneRequests) and self.__queue.isEmpty and isAllNone(self.__runways)


	def toString(self):
		output = 'The time is currently t = {0}.\n'.format(self.__currentTime)
		output += 'The runways:\n'
		runwayFormatString = '\t{0} is currently on runway {2} and will take off in {1} ticks.\n'
		emptyRunwayFormatString = '\tRunway {0} is currently empty.\n'
		queueFormatString = '\t{0}: Request submitted at t = {1} for t = {2}. Will take {3} ticks to take off. Is schedualed for runway {4} at t = {5}\n'


		runwayClearArray = []
		i = 0
		while i < len(self.__runways):
			plane = self.__runways[i]
			if plane is None:
				output += emptyRunwayFormatString.format(i)
				runwayClearArray.append(self.__currentTime)
			else:
				output += runwayFormatString.format(plane[1][0], plane[0] - self.__currentTime, i)
				runwayClearArray.append(plane[0])
			i += 1

		output += 'The request queue:\n'

		for entry in self.__queue.toArray():
			lane = getFirstMinIndex(runwayClearArray)
			output += queueFormatString.format(entry[0],entry[1],entry[2],entry[3], lane, runwayClearArray[lane])
			runwayClearArray[lane] += entry[3]
		
		return output
