from variable import *
import sys

class Solver:
	""" Class represents a general binary constraint problem solver. """

	def __init__(self, problem, ordering, task_type):
		""" Class constructor. 
		:param problem: what problem to solve 
		:param ordering: a flag marking what order to use for 
		variables, e.g. 0 for default, 1 for small domain first
		:param task_type: what problem we are solving (string) """
		# ordering is int to allow further options
		# task_type only necessary for comfortable printing out
		self.problem = problem
		self.n = len(problem.variables)
		self.ordering = ordering
		# we will be working with this list
		# created just in case, don't really need it
		self.copiedVariables = list(self.problem.variables)
		self.assignedVariables = []
		self.task_type = task_type

	def getNextVariable(self):
		""" Depending on the ordering we decided in the beginning
		(it can be changed at any point), choose the next variable. """
		if self.ordering==0:
			# default
			return self.getVariableByDepth()
		else:
			if self.ordering==1:
				# dynamic
				return self.getVariableByDomain()
			else:
				# another option?
				pass

	def getVariableByDepth(self):
		""" Get the next variable from the list of
		unassigned variables and put it into the list of assigned variables. """
		res = self.copiedVariables.pop(0) 
		self.assignedVariables.append(res)
		return res

	def getVariableByDomain(self):
		""" Choose a variable with the smallest domain and move it from 
		the list of unssigned (copied) variables to the list 
		of assigned ones. """
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
		""" Assign the given variable the given value 
		:param var: which variable to assign 
		:param value_index: index in the domain list of var 
		value = domain[value_index] will be assigned to var
		If the value is marked as impossible, assign None."""
		if var.domain.flags[value_index] is not "X":
			var.value = var.domain.values[value_index]
		else: 
			var.value = None

	def findConstraint(self, var1, var2):
		""" Finds a constraint about two variables by finding them in the 
		expressions of the given constraints. """
		for constraint in self.problem.constraints:
			if isinstance(constraint, ExpressionConstraint):
				if findVarName(constraint.lhs) == var1.name and findVarName(constraint.rhs) == var2.name:
					return constraint
			else:
				if constraint.lhs.name == var1.name and constraint.rhs.name == var2.name:
					return constraint
		return None

	def revise(self, future, present):
		""" 
		:param future: the future variable that we are revising
		:param  present: variable that was just assigned a value 
		This method finds a constraint for these two variables,
		then goes through the domain of the future variabl eand substitutes the values.
		Values that do no satisfy the constraint are marked as not possible.
		If the domain of the future variable becomes empty, a false value is returned.
		The removed list accumulates values for each variable that were removed from the 
		domain. If something is inconsistent, the changes will be undone based on this list. """
		removed = []
		constraint = self.findConstraint(future, present)
		if constraint is None:
			# variables do not depend on each other
			return (True, removed)
		else:
			domain_not_empty = False
			for index in range(len(future.domain.values)):
				# check every value in the domain of the future variable
				if future.domain.flags[index] != "X":
					# only check possible values
					satisfies = constraint.valuesSatisfy(future.domain.values[index], present.value)
					if not satisfies:
						# remove from the domain
						future.domain.flags[index] = "X"
						removed.append((future, index)) # append the index of the pruned value
					else:
						domain_not_empty = True 
		return (domain_not_empty, removed)

	def showSolution(self):
		""" Prints the solution of the problem. Generally, 
		prints a list of variables with assigned values.
		For sudoku, prints a grid. """
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
		""" Undoes the changes beased on the change list, then 
		moves the variables back to the unassigned (copied) list.
		:param change_list: list of a format [(variable, value_index),...]
		e.g. [(v1,0)] means that for v1, value indexed by 0 (which is 1 for 
			a sudoku domain) was removed.
		:param num_assignments: how many variables to "unassign"
		"""
		for index in range(len(change_list)):
			var = change_list[index][0]
			var.domain.flags[change_list[index][1]]="new"
		for n in range(num_assignments):
			self.undo_assignment()

	def undo_assignment(self):
		""" Undoes an assignment by taking the last assigned variable 
		and putting it in front of the unassigned (copied) list. """
		lastAssigned = self.assignedVariables.pop(-1) 
		self.copiedVariables = [lastAssigned] + self.copiedVariables

	def print_state_short(self):
		""" Prints state by printing all variables with their domains and flags. """
		for var in self.problem.variables:
			for index in range(len(var.domain.values)):
				print var.name + ": " + str(var.domain.values[index]) + ", " + var.domain.flags[index]

	def print_state(self):
		""" prints state by printing variables with (value, flag) grouped together """
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
		""" Prints already assigned variables and then not yet assigned. """
		print "assignedVariables: ",
		print [var.name for var in self.assignedVariables]
		print "still to assign:",
		print [var.name for var in self.copiedVariables]


	def forwardCheck(self, depth):
		""" Main forward schecking algorithm.
		:param depth: the current depth of the search tree. """
		var = self.getNextVariable()
		# check every value in the available domain of the variable
		for value_index in range(len(var.domain.values)):
			self.assign(var, value_index)
			if var.value is None:
				# this value is not in the domain anymore
				continue
			# print "-> " + var.name + " = " + str(var.value) + " "
			consistent = True
			future = 0
			removed = []
			for future in range(depth+1, self.n):
				result = self.revise(self.getNextVariable(), var)
				# add new changes to the list
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
					# variable on depth + 1. This means that this is inconsistent
			if (future < self.n - 1):
				self.undoPruning(removed, future - depth)
			else:
				self.undoPruning(removed, 1)
		# at this point the values in the domain ended 
		# with no success, so need to backtrack
		# from here the execution will return to line 
			