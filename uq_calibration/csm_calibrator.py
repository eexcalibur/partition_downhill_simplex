import pool
import config
import scheduler

if __name__ == '__main__':
	cases_num  = config.cases_num
	hosts_file = config.hosts_file
	windows_size = config.windows_size

	# init job queue
	job_q = []    # get a queue
	for i in range(config.restart_case, cases_num+1) :
		job_q.append(i)

	#init nodes pool
	pool_res = pool.Pool()
	pool_res.set_pool()

	#init job scheduler
	job_scheduler=scheduler.Scheduler()
	#assign a job for avail nodes
	
	while len(job_q):
		if pool_res.get_avail_cores() and pool_res.ass_jobs_num < windows_size:
			work_id=job_q.pop(0)
			pool_res.ass_jobs_num = pool_res.ass_jobs_num + 1
			#running model
			#print job_scheduler.job_reg
			job_scheduler.run_model(work_id, pool_res.avail_res)
		else :
			job_scheduler.check_run_model(pool_res)


#	pool_res.get_avail_cores()
#	print pool_res.avail_res.keys()
