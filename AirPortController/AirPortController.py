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
		self.__queue = PriorityQueue.PriorityQueue(CreateComparetor([(2, False), (1, False), (3, False)], False))
		self.__time = 0
		self.__currentPlane = None # (end time, request)

