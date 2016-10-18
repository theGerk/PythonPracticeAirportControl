import PriorityQueue


def isAllNone(input):
	for elem in input:
		if elem is not None:
			return False
	return True


def getFirstIndexlessThenOrEqualToXOrIsLeastValueIfThereIsNonelessThenOrEqualToX(input, x):
	if not (len(input) > 0):
		return None
	elif input[0] <= x:
		return 0
	minIndex = 0
	i = 1
	while i < len(input):
		if input[i] < input[minIndex]:
			if i <= x:
				return i
			minIndex = i
		i += 1
	return minIndex


class AirportController: 
	def __init__(self, airplaneRequests, lanes):
		self.__airplaneRequests = airplaneRequests
		self.__currentIndexInAirplaneRequests = 0
		self.__queue = PriorityQueue.PriorityQueue(PriorityQueue.CreateComparetor([('requested time', False), ('submission time', False), ('take off time', False)], False))
		self.__currentTime = -1
		self.__runways = [None] * lanes # [{"end time", "request"}]


	def tick(self):
		self.__currentTime += 1
		changeDetected = False

		#move planes out of runways if they are done taking off
		i = 0
		while i < len(self.__runways):
			if self.__runways[i] is not None and self.__runways[i]['end time'] == self.__currentTime:
				self.__runways[i] = None
				changeDetected = True
			i += 1

		#add new requests into queue
		while self.__currentIndexInAirplaneRequests < len(self.__airplaneRequests):
			airplane = self.__airplaneRequests[self.__currentIndexInAirplaneRequests]
			if airplane['submission time'] == self.__currentTime:
				self.__queue.insert(airplane)
				changeDetected = True
			else:
				break
			self.__currentIndexInAirplaneRequests += 1

		#move new planes into runway
		i = 0
		while i < len(self.__runways):
			peek = self.__queue.peek
			if self.__runways[i] is None and peek is not None and peek['requested time'] <= self.__currentTime:
				tmp = self.__queue.take()
				self.__runways[i] = {'end time': tmp['take off time'] + self.__currentTime, 'request': tmp}
				changeDetected = True
			elif peek is None or peek['requested time'] > self.__currentTime:
				break
			i += 1

		return changeDetected

	@property
	def isComplete(self):
		return self.__currentIndexInAirplaneRequests >= len(self.__airplaneRequests) and self.__queue.isEmpty and isAllNone(self.__runways)


	def toString(self):
		output = 'The time is currently t = {0}.\n'.format(self.__currentTime)
		output += 'The runways:\n'
		runwayFormatString = '\t{2}: {0} will take off in {1} ticks.\n'
		emptyRunwayFormatString = '\t{0}: Is currently empty.\n'
		queueFormatString = '\t{6}: {0} submitted request at t = {1} for t = {2}. Will take {3} ticks to take off. Is schedualed for runway {4} at t = {5}\n'


		runwayClearArray = []
		i = 0
		while i < len(self.__runways):
			plane = self.__runways[i]
			if plane is None:
				output += emptyRunwayFormatString.format(i)
				runwayClearArray.append(self.__currentTime)
			else:
				output += runwayFormatString.format(plane['request']['name'], plane['end time'] - self.__currentTime, i)
				runwayClearArray.append(plane['end time'])
			i += 1

		output += 'The request queue:\n'

		myQueue = self.__queue.toArray()
		for i in range(self.__queue.elements):
			entry = myQueue[i]
			lane = getFirstIndexlessThenOrEqualToXOrIsLeastValueIfThereIsNonelessThenOrEqualToX(runwayClearArray, entry['requested time'])
			runwayClearArray[lane] = max(runwayClearArray[lane], entry['requested time'])
			output += queueFormatString.format(entry['name'],entry['submission time'],entry['requested time'],entry['take off time'], lane, runwayClearArray[lane], i)
			runwayClearArray[lane] += entry['take off time']
		
		return output
