"""
Airport controller class, specifically made for this project.
See it's doucmentation for further details.
"""
import PriorityQueue


def isAllNone(input):
	"""
	input -> any iteratable object

	Returns if every element in input is None.
	"""
	for elem in input:
		if elem is not None:
			return False
	return True


def getFirstIndexLessThenOrEqualToXOrIsLeastValueIfThereIsNoneLessThenOrEqualToX(input, X):
	"""
	input -> list or tuple of values comparable by '<' and '<=' operators
	X -> a value that could exist in the list
	
	Returns the first index that has a value less then or equal to X in input.
	If there are none then it returns the index at which the value is least.
	Returns None if the list is empty.
	"""
	#none if list is empty
	if not (len(input) > 0):
		return None

	#returns the first element if it's less then X
	elif input[0] <= X:
		return 0

	#assume minIndex is 0
	minIndex = 0

	#check each other index
	for i in range(1, len(input)):
		if input[i] < input[minIndex]:
			if i <= X:
				return i
			minIndex = i

	#returns after not finding anything less or equal to then X
	return minIndex



def lineToRequst(line):
	"""
	line -> string in format "name, submission time, requested time, take off time"

	returns dictionary with name of feild refering the value
	"""
	a = line.split(',')
	return {"name": a[0], "submission time": int(a[1]), "requested time": int(a[2]), "take off time": int(a[3])}


class AirportController: 
	"""
	Represents an airport, takes a list of requests and a number lanes and then can be ticked through.
	To string outputs it's current state in human readable form
	"""

	def __init__(self, airplaneRequests, lanes = 1):
		"""
		airplaneRequests:
			string formated as "name, submission time, requested time, take off time" repeated for as many requests as there are, with newlines between.
			list of strings formated as "name, submssion time, requested time, take off time"
		lanes -> integer greater then 0, defaults to 1
		"""

		#if airplaneRequests is a string
		if isinstance(airplaneRequests, str):
			self.__airplaneRequests = []
			for line in airplaneRequests.split('\n'):
				if len(line) > 1:
					self.__airplaneRequests.append(lineToRequst(line))

		#if airplaneRequests is a list
		elif isinstance(airplaneRequests, list):
			self.__airplaneRequests = [lineToRequst(line) for line in airplaneRequests]		#expected to be in correct format


		self.__currentIndexInAirplaneRequests = 0
		self.__queue = PriorityQueue.PriorityQueue(PriorityQueue.CreateComparetor([('requested time', False), ('submission time', False), ('take off time', False)], False))
		self.__currentTime = -1
		self.__runways = [None] * lanes # [{"end time", "request"}]

	
	def multiStep(self):
		"""
		ticks until a change happens, should do this more efficently then tick function.
		does nothing if the airport is complete
		returns number of ticks completed
		"""

		if self.isComplete():
			return 0

		#plane leaving runway
		moveTimeTo = min(self.__runways, key = lambda runway: runway['end time'])['end time']

		#new requests enter queue
		if self.__currentIndexInAirplaneRequests < len(self.__airplaneRequests):
			airplane = self.__airplaneRequests[self.__currentIndexInAirplaneRequests]
			if airplane['submission time'] < moveTimeTo:
				moveTimeTo = airplane['submission time']

		#move plane into runway
		peek = self.__queue.peek
		if None in runway and peek is not None:
			if peek['requested time'] < moveTimeTo:
				moveTimeTo = peek['requested time']

		#set time to one less then target
		output = moveTimeTo - currentTime
		self.currentTime = moveTimeTo - 1
		
		#do stuff
		self.step()
		return output


	def step(self):
		"""
		increments time by 1, and then does all logic that would be done at that time.
		returns if any of the bellow have happened:
			a new plane has been added to the queue
			a plane has been removed from a runway
			a plane is being added to the runway
		"""
		self.__currentTime += 1
		changeDetected = False

		#move planes out of runways if they are done taking off
		for i in range(len(self.__runways)):
			if self.__runways[i] is not None and self.__runways[i]['end time'] == self.__currentTime:
				self.__runways[i] = None
				changeDetected = True

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
		for i in range(len(self.__runways)):
			peek = self.__queue.peek
			if self.__runways[i] is None and peek is not None and peek['requested time'] <= self.__currentTime:
				tmp = self.__queue.pop()
				self.__runways[i] = {'end time': tmp['take off time'] + self.__currentTime, 'request': tmp}
				changeDetected = True
			elif peek is None or peek['requested time'] > self.__currentTime:
				break

		return changeDetected

	@property
	def isComplete(self):
		"""
		returns if the airport object is finished being used (is passed the amount of time at which anything new will happen)
		"""
		return self.__currentIndexInAirplaneRequests >= len(self.__airplaneRequests) and self.__queue.isEmpty and isAllNone(self.__runways)


	def toString(self):
		"""
		returns the object as a string formated to be human readable with all important information.

		First outputs current time.
		Then outputs information about planes in each runway.
		Then outputs information about each plane in the queue, and when they are going to take off and from what lane.
		"""

		#format strings
		runwayFormatString = '\t{2}: {0} will take off in {1} ticks.\n'
		emptyRunwayFormatString = '\t{0}: Is currently empty.\n'
		queueFormatString = '\t{6}: {0} submitted request at t = {1} for t = {2}. Will take {3} ticks to take off. Is schedualed for runway {4} at t = {5}\n'


		#start building ouptut
		output = 'The time is currently at t = {0}.\n'.format(self.__currentTime)
		output += 'The runways:\n'


		#array of times at which each runway will be empty again
		runwayClearArray = []

		#build output for the current runways and build runwayClearArray
		for i in range(len(self.__runways)):
			plane = self.__runways[i]
			if plane is None:	#there is no plane in this runway
				output += emptyRunwayFormatString.format(i)
				runwayClearArray.append(self.__currentTime)
			else:				#there is a plane in this runway
				output += runwayFormatString.format(plane['request']['name'], plane['end time'] - self.__currentTime, i)
				runwayClearArray.append(plane['end time'])


		output += 'The request queue:\n'


		myQueue = self.__queue.toList()		#the array containing all elements in the queue


		#iterate across elements in the queue (does not use		for entry in self.__queue.toArray()		as we need the index to be known)
		for i in range(self.__queue.elements):
			entry = myQueue[i]

			#computes which runway lane the current plane is being schedualed to use
			lane = getFirstIndexLessThenOrEqualToXOrIsLeastValueIfThereIsNoneLessThenOrEqualToX(runwayClearArray, entry['requested time'])

			#update runwayClearArray, to being the the value at which the current plane will get onto it
			runwayClearArray[lane] = max(runwayClearArray[lane], entry['requested time'])

			#add into output
			output += queueFormatString.format(entry['name'],entry['submission time'],entry['requested time'],entry['take off time'], lane, runwayClearArray[lane], i)

			#add the amount of time needed to take off to this runway's entry in runwayClearArray
			runwayClearArray[lane] += entry['take off time']
		


		return output
