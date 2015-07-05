import numpy
import math
import copy
import logging
import block
import task_queue
import uq_calibration.config as config
import uq_calibration.pool as pool

def init_logging():
	logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='pdso.log',
                filemode='w')

	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
								  '%a, %d %b %Y %H:%M:%S')
	console.setFormatter(formatter)
	logging.getLogger('').addHandler(console)


def partition_range(q, range_data, num_avail_res, dix, diy):
	#part_factor = int(math.floor(num_avail_res ** 0.5))
	part_factor = int(math.floor(config.blocks_num ** 0.5))
	ndx = part_factor 
	while (ndx > 1 and config.blocks_num % ndx != 0 ):
		ndx = ndx - 1
	ndy = config.blocks_num / ndx
	sdx = (range_data[dix][1] - range_data[dix][0]) / ndx
	sdy = (range_data[diy][1] - range_data[diy][0]) / ndy

	print ndx, ndy
	new_range = copy.deepcopy(range_data)
	for idx in range(0, ndx):
		new_range[dix][0] = range_data[dix][0]+idx * sdx
		new_range[dix][1] = new_range[dix][0] + sdx
		for idy in range(0, ndy):
			new_range[diy][0] = range_data[diy][0]+ idy * sdy
			new_range[diy][1] = new_range[diy][0] + sdy
			q.queue.append(block.block(new_range))  



if __name__ == '__main__':

	#init log
	init_logging()

	#read the init range
	init_range = numpy.loadtxt("range_init")

	#partition the init range
	pool_res = pool.Pool()
	pool_res.set_pool()

	#push blocks into queue
	task_q = task_queue.task_queue()
	partition_range(task_q, init_range, pool_res.num_avail_res, 0, 1)


	#while (len(task_q.queue) != 0):
	task_q.start_tasks()
	task_q.write_hist()

