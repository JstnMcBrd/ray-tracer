"""
Add-ons to the builtin `multiprocessing` library.
"""


# This implementation is rather hacked and causes a lot of warnings and errors
# that are inherent and cannot be resolved. So until I design something better,
# I will disable linting for this file.

# pylint: disable=all

from multiprocessing.pool import IMapIterator, Pool, starmapstar
from typing import Callable


def istarmap(pool: Pool, func: Callable, iterable: list, chunksize=1):
	"""
	`starmap` version of `imap` for Python 3.8+.
	Adopted this from [this source](https://stackoverflow.com/a/57364423).
	"""

	pool._check_running()
	if chunksize < 1:
		raise ValueError(f"Chunksize must be 1+, not {chunksize}")

	task_batches = Pool._get_tasks(func, iterable, chunksize)
	result = IMapIterator(pool)
	pool._taskqueue.put(
		(
			pool._guarded_task_generation(result._job, starmapstar, task_batches),
			result._set_length
		)
	)
	return (item for chunk in result for item in chunk)
