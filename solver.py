from variable import *
import sys

class Solver:
	def __init__(self, problem, ordering, task_type):
		self.problem = problem
		self.n = len(problem.variables)
		self.ordering = ordering
		self.copiedVariables = list(self.problem.variables)
		self.assignedVariables = []
		self.task_type = task_type

	def getNextVariable(self):
		if self.ordering==0:
			# default
			return self.getVariableByDepth()
		else:
			if self.ordering==1:
				# dynamic
				return self.getVariableByDomain()
			else:
				# mb static given by user
				pass

	def getVariableByDepth(self):
		res = self.copiedVariables.pop(0) # this pop works
		self.assignedVariables.append(res)
		return res

	def getVariableByDomain(self):
		min_domain = len(self.copiedVariables[0].domain.values)
		min_domain_index = 0
		for index in range(len(self.copiedVariables)):
			variable = self.copiedVariables[index]
			domain_size = 0
			for value_index in range(len(variable.domain.values)):
				if variable.domain.flags[value_index] != "X":
					domain_size += 1
			if domain_size < min_domain:
				min_domain = domain_size
				min_domain_index = index
		res = self.copiedVariables.pop(min_domain_index) # this pop works
		self.assignedVariables.append(res)
		return res 


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
			# variables do not depend on each other
			return (True, removed)
		else:
			domain_not_empty = False
			for index in range(len(future.domain.values)):
				if future.domain.flags[index] != "X":
					satisfies = constraint.valuesSatisfy(future.domain.values[index], present.value)
					if not satisfies:
						future.domain.flags[index] = "X"
						removed.append((future, index)) # append the index of the pruned value
					else:
						domain_not_empty = True 
		return (domain_not_empty, removed)

	def showSolution(self):
		print "|Solution:======================================================================"
		if self.task_type=="sudoku":
			for i in range(9):
				for j in range(9):
					print str(self.problem.variables[i*9+j].value) + " ",
				print "\n"
		else:
			for var in self.problem.variables:
				print "|" + var.name + ": " + str(var.value)
			print "|_________"

	def undoPruning(self, change_list, num_assignments):
		for index in range(len(change_list)):
			var = change_list[index][0]
			var.domain.flags[change_list[index][1]]="new"
		for n in range(num_assignments):
			self.undo_assignment()

	def undo_assignment(self):
		lastAssigned = self.assignedVariables.pop(-1) 
		self.copiedVariables = [lastAssigned] + self.copiedVariables

	def print_state_short(self):
		for var in self.problem.variables:
			for index in range(len(var.domain.values)):
				print var.name + ": " + str(var.domain.values[index]) + ", " + var.domain.flags[index]

	def print_state(self):
		print "STATE:______"
		for var in self.problem.variables:
			print var.name + ": ",
			for index in range(len(var.domain.values)):
				if var.domain.flags[index] == "X":
					symbol = "X"
				else:
					symbol = str(var.domain.values[index])
				print symbol + ", ",
			print " "
		print "__________"

	def print_vars(self):
		print "assignedVariables: ",
		print [var.name for var in self.assignedVariables]
		print "still to assign:",
		print [var.name for var in self.copiedVariables]


	def forwardCheck(self, depth):
		var = self.getNextVariable()
		for value_index in range(len(var.domain.values)):
			#print "depth " + str(depth)
			self.assign(var, value_index)
			if var.value is None:
				continue
			# print "-> " + var.name + " = " + str(var.value) + " "
			consistent = True
			future = 0
			removed = []
			for future in range(depth+1, self.n):
				result = self.revise(self.getNextVariable(), var)
				removed.extend(result[1])
				consistent = result[0]
				if not consistent:
					break
			if consistent:
				if depth == self.n - 1:
					self.showSolution()
				else:
					for future in range(depth+1, self.n):
						self.undo_assignment()
					self.forwardCheck(depth+1)
					# if we are here, it means that variables finished for the
					# next variable. This means that this is inconsistent
			if (future < self.n - 1):
				self.undoPruning(removed, future - depth)
			else:
				self.undoPruning(removed, 1)
		# at this point the values in the domain ended 
		# with no success, so need to backtrack 
			