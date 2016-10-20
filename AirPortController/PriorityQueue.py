"""
Mainly the PriorityQueue class, but also a function to create basic compareators for it.
"""


class PriorityQueue:
	"""
	A very generalized priority queue class.
	Bases location of inputed values on compareFunction.
	Allows for accumulator to be used to store data between calls of compare function.
	"""

	#every node is stored as a list with 2 elements, the 0th element is the value, and the 1st elment is the next node.
	
	def __init__(self, compareFunction, initialAccumulator = {}):
		"""
		compareFunction is a function of 3 arguments, and returns if the first argument should be before the second argument as a boolean, the third argument is an acumulator object that can be used to store whatever is desired, and is passed into each calling of the function
		Before every insert the accumulator is set the initialAccumulator's value.
		"""

		self.__compare = compareFunction				#the comparetor function
		self.__initialAccumulator = initialAccumulator	#the initial value for the accumulator
		self.__elements = 0								#the number of elements in the queue
		self.__queue = [None, None]						#an element that goes before the head, index 1 will point to the first element. Can be thought of as our head pointer.


	def __insert(self, newNode):
		"""
		inserts an element into the priority queue, does not increment the number of elements, (private function)
		"""
		previous = self.__queue			#previous is set the the element before the head
		current = previous[1]			#current is set to the first element in the linked list
		accumulator = self.__initialAccumulator
		while True:
			if (current is None) or (self.__compare(newNode, current[0], accumulator)):
				previous[1] = [newNode, current]
				break
			previous = current
			current = current[1]
		
	def insert(self, newNode):
		"""
		inserts an element into the priority queue and then increments the number of elements.
		"""
		self.__insert(newNode)
		self.__elements += 1

	def __take(self):
		"""
		Takes out the first element of the queue, and returns it without decrementing the number of elements.
		"""
		head = self.__queue
		
		#if the queue is empty then return None
		if head[1] is None:
			return None

		#otherwise repoint to the next object and reutrn the first.
		else:
			output = head[1][0]
			head[1] = head[1][1]
			return output

	def pop(self):
		"""
		pops the first element out of the queue, and decrements the number of elements.
		returns the element that was poped.
		"""
		self.__elements -= 1
		return self.__take()

	def toList(self):
		"""
		Returns the contents of the queue as an array. 
		"""
		current = self.__queue[1]
		output = []
		while current is not None:
			output.append(current[0])
			current = current[1]
		return output

	@property
	def elements(self):
		"""
		Returns the number of elements in the queue, assuming you didn't do something stupid.
		"""
		return self.__elements

	def insertMultiple(self, values):
		"""
		inserts multiple elements more efficently then if insert was called repeatedly.

		values is some iteratable object that contains elements to be added to the queue.
		"""
		for n in values:
			self.__insert(n)
		self.__elements += n

	@property
	def peek(self):
		"""
		returns the first value in the queue, without messing with the queue at all.
		"""
		if self.__queue[1] is None:
			return None
		else:
			return self.__queue[1][0]

	def popMultiple(self, number):
		"""
		Pops multiple values from the queue more efficently then calling pop multiple times.
		Returns them all in a list.
		"""
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
		"""
		returns if the queue has elements in it.
		"""
		return self.__elements == 0




def CreateComparetor(argumentArray, firstGetsPreference):
	"""
	Returns a simple comparator function that only is based on elements within the arguments that are only compared using greater then operator.
	It will give the preference to which ever is greater (or less depending on what is specified) in the index, and if they are equal it defers to the next index specified.
	If all indecies contain equal values then the firstGetsPreference comes into play.

	Specifically made to be used with PriorityQueue class, although can be used elsewhere.


	argumentArray in form of tuples, with first entry being the index name, the second being a boolean
                                                                                   True => greater gets precedence
                                                                                   False => lesser gets precedence
	firstGetsPreference is a boolean, representing what it's name implies.
	"""
	def output(a, b, acumulator = None):
		"""
		Dynamically created comparetor function.
		"""
		for arg in argumentArray:
			if a[arg[0]] != b[arg[0]]:
				return (a[arg[0]] > b[arg[0]]) == arg[1]
		return firstGetsPreference
	return output
