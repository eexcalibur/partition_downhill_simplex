import copy
import numpy

class block(object):
	"""docstring for Block"""
	def __init__(self, range):
		self.subrange = copy.deepcopy(range)
		self.final_optimal = float("inf")
		self.current_optimal = float("inf")
		self.iteration_nums = 0
		self.status = 0 # 0=initial 1=running 2=finishing

#	def __cmp__(self, other):
#		return cmp(self.current_optimal, other.current_optimal)
	
	def run_block(self):
		numpy.savetxt("algorithm/subrange", self.subrange)