import numpy
import math
import sys
import copy
import logging
import block
import task_queue
import partition_range
import uq_calibration.config as config


def init_logging():
	logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s  [%(levelname)s] %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='pdso.log',
                filemode='w')

	console = logging.StreamHandler()
	console.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s  [%(levelname)s] %(message)s',
								  '%a, %d %b %Y %H:%M:%S')
	console.setFormatter(formatter)
	logging.getLogger('').addHandler(console)

	sys.setrecursionlimit(1000000)
 

if __name__ == '__main__':

	#init log
	init_logging()

	#push blocks into queue
	task_q = task_queue.task_queue()

	#partition the init range
	part = partition_range.partition_range()
	part.part_range()
	part.merge_range(part.part_list, task_q, 0)

	task_q.start_tasks()
	task_q.write_hist()

