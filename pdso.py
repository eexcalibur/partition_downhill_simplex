import numpy
import math
import Queue as Q
import uq_calibration.config as config
import uq_calibration.pool as pool

if __name__ == '__main__':
	#read the init range
	init_range = numpy.loadtxt("range_init")
	para_num   = len(init_range)

	#partition the init range
	pool_res = pool.Pool()
	pool_res.set_pool()
	part_factor = int(math.floor(pool_res.num_avail_res ** 0.5))

	
	

	q = Q.PriorityQueue()



