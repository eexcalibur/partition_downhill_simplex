import numpy
import uq_calibration.config as config 

class partition_range(object):
	"""docstring for range"""
	def __init__(self):
		self.init_range = numpy.loadtxt("range_init")
		self.part_list  = []
		self.para_num   = len(self.init_range)
		self.block_num  = config.part_factor ** self.para_num
		self.m_range = [0 for i in range(self.para_num)]

	def part_range(self):		
		for i in range(0, self.para_num):
			p1_range = []
			sd = (self.init_range[i][1] - self.init_range[i][0]) / config.part_factor

			for j in range(0, config.part_factor):
				p1_sub_range = [0, 0]
				p1_sub_range[0] = self.init_range[i][0] + j * sd
				p1_sub_range[1] = p1_sub_range[0] + sd
				p1_range.append(p1_sub_range)

			self.part_list.append(p1_range)

	
	def merge_range(self, part_data, q, idim):
		if(idim == self.para_num):
			print self.m_range
			q.queue.append(block.block(self.m_range))
			return

		for i in range(0, config.part_factor):
			self.m_range[idim] = part_data[idim][i]
			self.merge_range(part_data, idim+1)


		