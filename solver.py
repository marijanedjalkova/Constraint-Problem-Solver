from variable import *

class Solver:
	def __init__(self, problem, ordering):
		self.problem = problem
		self.n = len(problem.variables)
		self.ordering = ordering
		if ordering == 1:
			# create a copy of the list

	def getNextVariable(self, depth):
		if self.ordering==0:
			# default
			return self.getVariableByDepth(depth)
		else:
			if self.ordering==1:
				# dynamic
				return self.getVariableByDomain()
			else:
				# mb static given by user
				pass

	def getVariableByDepth(self, depth):
		return self.problem.variables[depth]

	def getVariableByDomain(self):
		min_domain = len(self.problem.variables[0])
		min_domain_index = 0
		for index in range(len(self.problem.variables)):
			variable = self.problem.variables[index]
			domain_size = 0
			for value in variable.domain:
				if value.flag != "X":
					domain_size += 1
			if domain_size < min_domain:
				min_domain = domain_size
				min_domain_index = index
		return min_domain_index # TODO need to delete it from the list of variables!


	def assign(self, var, value_index):
		if var.domain.flags[value_index] is not "X":
			var.value = var.domain.values[value_index]
		else: 
			var.value = None

	def findConstraint(self, var1, var2):
		for constraint in self.problem.constraints:
			if isinstance(constraint, ExpressionConstraint):
				if findVarName(constraint.lhs) == var1.name and findVarName(constraint.rhs) == var2.name:
					return constraint
			else:
				if constraint.lhs.name == var1.name and constraint.rhs.name == var2.name:
					return constraint
		return None

	def revise(self, future, present):
		# find the constraint about these two, 
		# mark the ones that do not satisfy with X, thus removing them from the domain
		# could do without Xs, but helps seeing
		# remember them in a list.
		# if anything has an empty domain, return false
		removed = []
		constraint = self.findConstraint(future, present)
		if constraint is None:
			# all fine, the veraibles do not depend on each other
			print "No constraints for " + future.name + " and " + present.name
			return (True, removed)
		else:
			domain_not_empty = False
			# var2 now has a value. So have to revise the domain of var1
			for index in range(len(future.domain.values)):
				satisfies = constraint.valuesSatisfy(future.domain.values[index], present.value)
				print str(future.domain.values[index]) + " and " + str(present.value) + " " +str(satisfies) + " the constraint",
				print_constraint(constraint)
				if not satisfies:
					print str(future.domain.values[index]) + " -> X"
					future.domain.flags[index] = "X"
					removed.append(index) # append the index of the pruned value
				else:
				    domain_not_empty = True
		return (domain_not_empty, removed)

	def showSolution(self):
		print "|Solution:======================================================================"
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
		var = self.getNextVariable(depth)
		for value_index in range(len(var.domain.values)):
			self.assign(var, value_index)
			if var.value is None:
				continue
			print "-> " + var.name + " = " + str(var.value)
			consistent = True
			for future in range(depth+1, self.n):
				print "FUTURE " + str(future)
				result = self.revise(self.getVariableByDepth(future), var)
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
			