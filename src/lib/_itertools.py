"Add-ons to the builtin `itertools` library."


import itertools


def closed_pairwise(iterable: list) -> itertools.pairwise:
	"""
	Similar to `itertools.pairwise`, but loops around to pair the first and last elements too.
	s -> (s0, s1), (s1, s2), (s2, s3), ..., (sn-1, sn), (sn, s0)
	"""

	return itertools.pairwise(itertools.chain(iterable, iterable[:1]))
