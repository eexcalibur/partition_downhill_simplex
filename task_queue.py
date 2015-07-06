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
		id = 1
		for b in self.queue:
			if pool_res.get_avail_cores() and pool_res.ass_jobs_num < config.windows_size:
				pool_res.ass_jobs_num = pool_res.ass_jobs_num + 1
				#job_scheduler.run_model(b, work_id, pool_res.avail_res)
				b.run_block(job_scheduler, id, pool_res.avail_res)
				logging.info("Processing the %d block. Best optimal: %e with %d iterations"  % (id, b.final_optimal, b.iteration_nums))
				id = id + 1
			else:
				#job_scheduler.check_run_model(pool_res)
				b.check_run_model(job_scheduler, pool_res)



	def write_hist(self):
		fp_fithist = file("fit_hist.txt", "wa")
		for b in self.queue:
			numpy.savetxt(fp_fithist, [b.final_optimal])
		fp_fithist.close();

		

