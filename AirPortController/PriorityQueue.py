class PriorityQueue:
	class SecretNodeType:
		def __init__(self, value, next):
			self.value = value
			self.next = next
	
	# compareFunction is a function of 2 arguments, and returns if the first argument should be before the second argument as a boolean.
	# compareFunction also may take 3 arguments, the third argument is an acumulator dictionary, that can be used to store whatever is desired, and is passed into each calling of the function
	# Before every insert the accumulator is set the initialAccumulator's value.
	def __init__(self, compareFunction, initialAccumulator = {}):
		self.__compare = compareFunction
		self.__accumulator = initialAccumulator
		self.__elements = 0
		self.__queue = SecretNodeType(None, None)
			
	def insert(self, newNode):
		previous = self.__queue
		current = previous.next
		while True:
			if (current is None) or (self.__compare(newNode, current.value, self.__accumulator)):
				previous.next = PriorityQueue.SecretNodeType(newNode, current)
				break
			previous = current
			current = current.next
		self.__accumulatorReseter(self.__accumulator)
		self.__elements += 1

	def take(self):
		if self.__next is None:
			return None
		else:
			tmp = self.__next
			self.__next = tmp.next
			self.__elements -= 1
			return tmp

	def toArray(self):
		current = self.__next
		output = []
		while current is not None:
			output.append(current.value)
			current = current.next
		return output

	@property
	def elements(self):
		return self.__elements

	def insertMultiple(self, nodes):
		for n in nodes:
			self.insert(n)
		self.__elements += len(nodes)

	def peek(self):
		return next.value

	def takeMultiple(self, number):
		self.__elements -= number
		if self.__elements < 0:
			self.__elements = 0
		return [self.take() for n in range(number)]
