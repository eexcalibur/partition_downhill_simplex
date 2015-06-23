import config

class Pool(object):
	"""docstring for Pool"""
	def __init__(self):
		self.pool_nodes = {}
		self.avail_res = {}
		self.num_avail_res = 0
		self.ass_jobs_num = 0
	
	def set_pool(self):
		#input_str = ""
		with open(config.hosts_file) as f:
			input_str = f.read()

		hosts_list = input_str.split('\n')
		
		#remove null element
		while '' in hosts_list:
			hosts_list.remove('')

		for host in hosts_list:
			self.pool_nodes[host] = config.core_per_host
		del hosts_list

		self.num_avail_res = len(self.pool_nodes) * config.core_per_host
#		print self.pool_nodes

#	def get_avail_nodes(self):
#		find_nodes=[]
#		find_nodes_num=0
#		self.avail_res=[]
#
#		for k,v in self.pool_nodes.items():
#			if (v == True):
#				find_nodes.append(k)
#				find_nodes_num += 1
#    			if (find_nodes_num == config.nodes_per_case):
#    				self.avail_res = find_nodes
#    				for x in range(len(find_nodes)):
#    					self.pool_nodes[find_nodes[x]] = False
#    				#print self.pool_nodes
#    				return True
#		return False

	def get_avail_cores(self):
		self.avail_res = {}	
		found_cores = 0 
		
		if (self.num_avail_res >= config.core_per_host):
			for k,v in self.pool_nodes.items():
				if (v != 0 ):
					if (found_cores + v < config.process_per_num) :
						found_cores += v
						self.avail_res[k] = v
						self.pool_nodes[k] = 0
					else :
						self.avail_res[k] = config.process_per_num - found_cores
						self.pool_nodes[k] = config.core_per_host - self.avail_res[k]
						#print self.pool_nodes
						#print self.avail_res
						return True
		return False
	


#	def reset_nodes(self, nodes_list):
#		for x in range(len(nodes_list)):
#			self.pool_nodes[nodes_list[x]] = True 

	def reset_cores(self, used_cores):
		for k,v in used_cores.items():
			self.pool_nodes[k] += v
