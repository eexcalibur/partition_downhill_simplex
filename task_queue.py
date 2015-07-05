import block
import numpy
import logging

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
		id = 1
		for b in self.queue:
			b.run_block()
			logging.info("Processing the %d block. Best optimal: %e with %d iterations"  % (id, b.final_optimal, b.iteration_nums))
			id = id + 1

	def write_hist(self):
		fp_fithist = file("fit_hist.txt", "wa")
		
		for b in self.queue:
			numpy.savetxt(fp_fithist, [b.final_optimal])

		fp_fithist.close();

