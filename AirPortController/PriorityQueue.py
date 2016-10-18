class PriorityQueue:
	# compareFunction is a function of 3 arguments, and returns if the first argument should be before the second argument as a boolean, the third argument is an acumulator object that can be used to store whatever is desired, and is passed into each calling of the function
	# Before every insert the accumulator is set the initialAccumulator's value.
	def __init__(self, compareFunction, initialAccumulator = {}):
		self.__compare = compareFunction
		self.__initialAccumulator = initialAccumulator
		self.__elements = 0
		self.__queue = [None, None]	# an element that goes before the head, index 1 will point to the first element. Can be thought of as our head pointer.


	def __insert(self, newNode):
		previous = self.__queue
		current = previous[1]
		accumulator = self.__initialAccumulator
		while True:
			if (current is None) or (self.__compare(newNode, current[0], accumulator)):
				previous[1] = [newNode, current]
				break
			previous = current
			current = current[1]
		
	def insert(self, newNode):
		self.__insert(newNode)
		self.__elements += 1

	def __take(self):
		head = self.__queue
		if head[1] is None:
			return None
		else:
			output = head[1][0]
			head[1] = head[1][1]
			return output

	def take(self):
		self.__elements -= 1
		return self.__take()

	def toArray(self):
		current = self.__queue[1]
		output = []
		while current is not None:
			output.append(current[0])
			current = current[1]
		return output

	@property
	def elements(self):
		return self.__elements

	def insertMultiple(self, nodes):
		for n in nodes:
			self.__insert(n)
		self.__elements += n

	@property
	def peek(self):
		if self.__queue[1] is None:
			return None
		else:
			return self.__queue[1][0]

	def takeMultiple(self, number):
		current = self.__queue[1]
		output = []
		for i in range(number):
			if current is None:
				break
			output.append(current[0])
			current = current[1]
		self.__queue[1] = current
		self.__elements -= len(output)
		return output

	@property
	def isEmpty(self):
		return self.__elements == 0



# argumentArray in form of tuples, with first entry being the index name, the second being a boolean
#                                                                                    True => greater gets precedence
#                                                                                    False => lesser gets precedence
def CreateComparetor(argumentArray, firstGetsPreference):
	def output(a, b, acumulator = None):
		for arg in argumentArray:
			if a[arg[0]] != b[arg[0]]:
				return (a[arg[0]] > b[arg[0]]) == arg[1]
		return firstGetsPreference
	return output
