lanes = 1	# the number of lanes we have is assumed to be 1, this may be changable in future versions of the project
import PriorityQueue

q = PriorityQueue.PriorityQueue(lambda x, y: x < y)
