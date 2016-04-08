class CSPSolver:
	def __init__(self, problem):
		self.problem = problem
		self.n = len(problem.variables)

	def getVariableByDepth(self, depth):
		return problem.variables[depth]

	def assign(self, var, value):
		var.value = value

	def revise(self, var1, var2):
		return True

	def showSolution(self):
		print "solution"

	def undoPruning(self):
		pass

	def forwardCheck(self, depth):
		var = getVariableByDepth(depth)
		for d in var.domain.values:
			assign(var, d)
			consistent = True
			for future in range(depth+1, n):
				while consistent:
					consistent = revise(getVariableByDepth(future), var)
			if consistent:
				if depth == n:
					showSolution()
				else:
					forwardCheck(depth+1)
			undoPruning()