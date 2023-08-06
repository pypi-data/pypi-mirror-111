import numpy as np

class Add3:
	def __init__(self, value, purpose):
		self.value = value
		self.purpose = purpose
	def get3more(self):
		return self.value + 3
	def sqrt(self):
		return np.sqrt(self.value)
	def get_purpose(self):
		return self.purpose
