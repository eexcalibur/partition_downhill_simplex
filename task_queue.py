import block

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
		for b in self.queue:
			b.run_block()
		