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

	#create init range
	def set_subrange(self, id): 
		#write initial range for each block
		paras_num = len(self.subrange)
		paras_init = [[0] * (paras_num + 1)] * paras_num

		for i in range(0, paras_num):
			paras_init[i] = numpy.random.rand(paras_num + 1) * (self.subrange[i][1] - self.subrange[i][0]) + self.subrange[i][0]

		fp_subrange = file("templete/subrange"+str(id), "wa")
		numpy.savetxt(fp_subrange, [1], fmt="%d")
		numpy.savetxt(fp_subrange, self.subrange)
		numpy.savetxt(fp_subrange,  numpy.transpose(paras_init))
		fp_subrange.close()


	def check_run_model(self, job_scheduler, pool_nodes):
		for k, v in job_scheduler.job_reg.items():
			cmd_status="ps -ef |grep CSM_work%d| grep -v grep" % k
			run_status=os.popen(cmd_status).readlines()
			if (len(run_status) == 0):
				#read result
				final_res = numpy.loadtxt("run/case%d/algorithms/downhill_simplex/final_res" % k)
				self.iteration_nums = final_res[0]
				self.final_optimal  = final_res[1]				
				# release nodes
				pool_nodes.reset_cores(v)
				# delete job_reg
				del job_scheduler.job_reg[k]
				pool_nodes.ass_jobs_num = pool_nodes.ass_jobs_num - 1

