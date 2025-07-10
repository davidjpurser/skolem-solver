

class Options: 

	
	def __init__(self, defaults = None):
		if defaults == None:
			self.options = {}
		else:
			self.options = defaults

	def set(self, options):
		for key in options:
			self.options[key] = options[key]


	def get(self, key, default = False):
		if key in self.options:
			return self.options[key]
		else:
			return default

	def set(self, key, value):
		self.options[key] = value
		return value

	def copy(self):
		return Options(self.options.copy())