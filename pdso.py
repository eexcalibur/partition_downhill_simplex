import numpy
import Queue as Q
import uq_calibration.config as config
import uq_calibration.pool as pool

if __name__ == '__main__':
	#read the init range
	init_range = numpy.loadtxt("range_init")
	
	#partition the init range
	pool_res = pool.Pool()
	pool_res.set_pool()
	print pool_res.num_avail_res

	q = Q.PriorityQueue()
	q.put(10)
	q.put(1)
	q.put(5)
	q.put(0.5)
	while not q.empty():
		print q.get()




