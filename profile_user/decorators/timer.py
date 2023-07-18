from functools import wraps
import time
from django.conf import settings

def timer(func):
	"""helper function to estimate view execution time"""
	@wraps(func)  # used for copying func metadata
	def wrapper(*args, **kwargs):
		# record start time
		start=time.time()

		# func execution
		result=func(*args, **kwargs)

		duration=(time.time() - start) * 1000
		# output execution time to console
		if settings.DEBUG:
			print(' Function {} takes {:.2f} ms'.format(
				func.__name__,
				duration
			))
		return result

	return wrapper