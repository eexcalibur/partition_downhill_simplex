import numpy
import math
import copy
import block
import Queue as Q
import uq_calibration.config as config
import uq_calibration.pool as pool

def partition_range(q, range_data, num_avail_res, dix, diy):
	part_factor = int(math.floor(num_avail_res ** 0.5))
	ndx = part_factor
	while (ndx > 1 and num_avail_res % ndx != 0 ):
		ndx = ndx - 1
	ndy = num_avail_res / ndx
	sdx = (range_data[dix][1] - range_data[dix][0]) / ndx
	sdy = (range_data[diy][1] - range_data[diy][0]) / ndy

	new_range = copy.deepcopy(range_data)
	for idx in range(0, ndx):
		new_range[dix][0] = range_data[dix][0]+idx * sdx
		new_range[dix][1] = new_range[dix][0] + sdx
		for idy in range(0, ndy):
			new_range[diy][0] = range_data[diy][0]+ idy * sdy
			new_range[diy][1] = new_range[diy][0] + sdy
			q.put(block.block(new_range))  



if __name__ == '__main__':
	#read the init range
	init_range = numpy.loadtxt("range_init")

	#partition the init range
	pool_res = pool.Pool()
	pool_res.set_pool()

	#push blocks into queue
	q = Q.PriorityQueue()	
	partition_range(q, init_range, pool_res.num_avail_res, 0, 1)

	

	
	



