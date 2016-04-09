class Solver:
	def __init__(self, problem):
		self.problem = problem
		self.n = len(problem.variables)

	def getVariableByDepth(self, depth):
		return self.problem.variables[depth]

	def assign(self, var, value_index):
		if var.domain.flags[value_index] is not "X":
			var.value = var.domain.values[value_index]

	def findConstraint(self, var1, var2):
		for constraint in self.problem.constraints:
			if constraint.variable1.name == var1.name and constraint.variable2.name == var2.name:
				return constraint
		return None

	def revise(self, future, present):
		# find the constraint about these two, 
		# mark the ones that do not satisfy with X, thus removing them from the domain
		# remember them in a list.
		# if anything has an empty domain, return false
		removed = []
		constraint = self.findConstraint(future, present)
		if constraint == None:
			# all fine, the veraibles do not depend on each other
			print "No constraints for " + future.name + " and " + present.name
			return (True, removed)
		else:
			domain_not_empty = False
			# var2 now has a value. So have to revise the domain of var1
			for index in range(len(future.domain.values)):
				satisfies = constraint.valuesSatisfy(present.value, future.domain.values[index])
				print str(present.value) + " and " + str(future.domain.values[index]) + " " +str(satisfies) + " the constraint"
				if not satisfies:
					print "XXX"
					future.domain.flags[index] = "X"
					removed.append(index) # append the index of the pruned value
				if future.domain.flags[index] is not "X" and domain_not_empty == False:
					domain_not_empty = True
		return (domain_not_empty, removed)

	def showSolution(self):
		print "|Solution:"
		for var in self.problem.variables:
			print "|" + var.name + ": " + str(var.value)
		print "|_________"

	def undoPruning(self, change_list, depth):
		var = self.problem.variables[depth]
		for index in change_list:
			var.domain.flags[index]="new"
		print var.domain.values
		print var.domain.flags
		print "pruning undone"

	def print_state(self):
		for var in self.problem.variables:
			for index in range(len(var.domain.values)):
				print var.name + ": " + str(var.domain.values[index]) + ", " + var.domain.flags[index]

	def print_state(self):
		print "STATE:______"
		for var in self.problem.variables:
			print var.domain.values
			print var.domain.flags
		print "__________"

	def forwardCheck(self, depth):
		print "DEPTH: " + str(depth)
		var = self.getVariableByDepth(depth)
		for value_index in range(len(var.domain.values)):
			self.assign(var, value_index)
			if var.value is None:
				continue
			print "-> " + var.name + " = " + str(var.value)
			consistent = True
			for future in range(depth+1, self.n):
				print "FUTURE " + str(future)
				result = self.revise(self.getVariableByDepth(future), var)
				self.print_state()
				removed = result[1]
				consistent = result[0]
				if not consistent:
					print "not consistent, backtrack"
					self.undoPruning(removed, future)
					break
			if consistent:
				if depth == self.n - 1:
					self.showSolution()
				else:
					self.forwardCheck(depth+1)
			