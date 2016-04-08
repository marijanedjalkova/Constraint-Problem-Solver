class Solver:
	def __init__(self, problem):
		self.problem = problem
		self.n = len(problem.variables)
		print "n is " + str(self.n)

	def getVariableByDepth(self, depth):
		return self.problem.variables[depth]

	def assign(self, var, value):
		var.value = value

	def revise(self, var1, var2):
		# go through rest of values, 
		# mark the ones that do not satisfy with X, thus removing them from the domain
		# remember them in a list or something. Or count the unmarked ones
		# if anything has an empty domain, return false
		return True

	def showSolution(self):
		print "|Solution:"
		for var in self.problem.variables:
			print "|" + var.name + ": " + str(var.value)
		print "|_________"

	def undoPruning(self):
		pass

	def forwardCheck(self, depth):
		print "depth is " + str(depth)
		var = self.getVariableByDepth(depth)
		print "got variable " + var.name + " value is " + str(var.value)
		for d in var.domain.values:
			self.assign(var, d)
			print "now " + var.name + " value is " + str(var.value)
			consistent = True
			for future in range(depth+1, self.n):
				print "future is " + str(future)
				consistent = self.revise(self.getVariableByDepth(future), var)
				if not consistent:
					break
			if consistent:
				if depth == self.n - 1:
					self.showSolution()
				else:
					self.forwardCheck(depth+1)
			self.undoPruning()