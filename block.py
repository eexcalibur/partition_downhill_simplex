import copy
import numpy, numpy.random
import os,sys
import logging

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
	
	def run_block(self, work_id, used_res):
		#write initial range for each block
		paras_num = len(self.subrange)
		paras_init = [[0] * (paras_num + 1)] * paras_num

		for i in range(0, paras_num):
			paras_init[i] = numpy.random.rand(paras_num + 1) * (self.subrange[i][1] - self.subrange[i][0]) + self.subrange[i][0] 

		fp_subrange = file("subrange", "wa")
		numpy.savetxt(fp_subrange, [1], fmt="%d")
		numpy.savetxt(fp_subrange, self.subrange)
		numpy.savetxt(fp_subrange,  numpy.transpose(paras_init))
		fp_subrange.close()

		#create mpd.hosts
		fp_host = open("mpd.hosts"+str(work_id), "w")
		for k, v in used_res.items():
			fp_host.write(k + ":"+ str(v) +"\n")
		fp_host.close()

		logging.info("work"+str(work_id)+" running on "+str(used_res.keys()))
		run_model_str="./run-model.sh CSM_work"+str(work_id)+" "+str(work_id)
		run_model_str += " &"

		os.system(run_model_str)
		self.job_reg[work_id] = used_res

		#run model
		#os.system("cd algorithms/downhill_simplex/; ./downhill_simplex")

		#read resualt
		final_res = numpy.loadtxt("algorithms/downhill_simplex/final_res")
		self.iteration_nums = final_res[0]
		self.final_optimal  = final_res[1]
		


	def run_model(self, work_id, used_res):











		
