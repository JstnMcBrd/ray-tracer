import multiprocessing.pool as mpp

def istarmap(self, func, iterable, chunksize=1):
	"""
	istarmap.py for Python 3.8+
	
	starmap version of imap
	Adopted this from [this source](https://stackoverflow.com/a/57364423)
	"""

	self._check_running()
	if chunksize < 1:
		raise ValueError("Chunksize must be 1+, not {0:n}".format(chunksize))

	task_batches = mpp.Pool._get_tasks(func, iterable, chunksize)
	result = mpp.IMapIterator(self)
	self._taskqueue.put(
		(
			self._guarded_task_generation(result._job, mpp.starmapstar, task_batches),
			result._set_length
		)
	)
	return (item for chunk in result for item in chunk)

# Add the method to the default multiprocessing library
mpp.Pool.istarmap = istarmap
