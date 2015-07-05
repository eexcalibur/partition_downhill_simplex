import copy
import numpy, numpy.random
import os

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
		paras_num = len(self.subrange)
		paras_init = [[0] * (paras_num + 1)] * paras_num

		for i in range(0, paras_num):
			paras_init[i] = numpy.random.rand(paras_num + 1) * (self.subrange[i][1] - self.subrange[i][0]) + self.subrange[i][0] 

		fp_subrange = file("algorithms/downhill_simplex/subrange", "wa")
		numpy.savetxt(fp_subrange, [1], fmt="%d")
		numpy.savetxt(fp_subrange, self.subrange)
		numpy.savetxt(fp_subrange,  numpy.transpose(paras_init))
		fp_subrange.close()

		os.system("cd algorithms/downhill_simplex/; ./downhill_simplex")






		
