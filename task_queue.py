import block
import numpy
import logging
import uq_calibration.pool as pool
import uq_calibration.scheduler as scheduler
import uq_calibration.config as config

class task_queue(object):
	"""docstring fos task_queue"""
	def __init__(self):
		self.queue = []
		self.queue_len = 0

	def get_priority(self):
		min_queue = self.queue[0]
		for q in self.queue:
			if(q.current_optimal < min_queue.current_optimal):
				min_queue = q 
		return min_queue

	def start_tasks(self):
		#set computing pool
		pool_res = pool.Pool()
		pool_res.set_pool()

		#init job scheduler
		job_scheduler=scheduler.Scheduler()

		#run all cases
		id = 0
		self.queue_len=len(self.queue)
		while (id < self.queue_len):
		#while (len(job_scheduler.job_reg) != 0):
			if pool_res.get_avail_cores() and pool_res.ass_jobs_num < config.windows_size:
				pool_res.ass_jobs_num = pool_res.ass_jobs_num + 1
				#job_scheduler.run_model(b, work_id, pool_res.avail_res)
				self.queue[id].id=id
				self.queue[id].set_subrange(id)
				job_scheduler.run_model(id, pool_res.avail_res)
				logging.info("Begin the %d block" % id)
				id = id + 1
			else:
				#job_scheduler.check_run_model(pool_res)
				job_scheduler.check_run_model(pool_res, self.queue)
		
		#check all block finished
		job_scheduler.check_all_exit(pool_res, self.queue)


	def write_hist(self):
		fp_fithist = file("fit_hist.txt", "wa")
		for b in self.queue:
			numpy.savetxt(fp_fithist, numpy.transpose([[b.id], [b.final_optimal], [b.iteration_nums]]))
		fp_fithist.close();

	
