import os
import pool
import config
import logging
import numpy

class Scheduler(object):
	"""docstring for Scheduler"""
	def __init__(self):
		self.job_reg = {}

	def run_model(self, work_id, used_res):
		fp_host = open("templete/mpd.hosts"+str(work_id), "w")
		for k, v in used_res.items():
			fp_host.write(k + ":"+ str(v) +"\n")
		fp_host.close()

		#print "work"+str(work_id)+" running on "+str(used_res.keys())
		run_model_str="./uq_calibration/run-model-window.sh CSM_work"+str(work_id)+" "+str(work_id)
		run_model_str += " &"
		#print run_model_str
		os.system(run_model_str)
		self.job_reg[work_id] = used_res

	def check_run_model(self, pool_nodes, queue_block):
		for k, v in self.job_reg.items():
			cmd_status="ps -ef |grep CSM_work%d| grep -v grep" % k
			run_status=os.popen(cmd_status).readlines()
			if (len(run_status) == 0):
				#read result
				final_res = numpy.loadtxt("run/case%d/algorithms/downhill_simplex/final_res" % k)
				queue_block[k].iteration_nums = final_res[0]
				queue_block[k].final_optimal  = final_res[1]
				logging.info("Finish the %d block. Best optimal: %e with %d iterations"  % (k, queue_block[k].final_optimal, queue_block[k].iteration_nums))

				# release nodes
				pool_nodes.reset_cores(v)
				# delete job_reg
				del self.job_reg[k]
				pool_nodes.ass_jobs_num = pool_nodes.ass_jobs_num - 1

	def check_all_exit(self, pool_res, queue_block):
		while(len(self.job_reg)):
			self.check_run_model(pool_res, queue_block)
		logging.info("All blocks have Finished!!!!!!!")



