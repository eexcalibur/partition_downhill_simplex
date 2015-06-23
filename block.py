class block(object):
	"""docstring for block"""
	def __init__(self, range):
		self.subrange = range
		self.final_optimal = float("inf")
		self.current_optimal = float("inf")
		self.iteration_nums = 0
		self.status = 1 # 1=running 0==finishing

	def __cmp__(self, other):
		return cmp(self.current_optimal, other.current_optimal)
		