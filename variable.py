"""This module contains classes for a constraint problem."""

import operator

class Variable:
	"""This class represents a variable for a CP (here and further - 
		constraint problem). """
	
	def __init__(self, name, domain):
		""" Variable constructor.
		:param name: name of a variable, a string 
		:param domain: a list of possible values of a variable
		Value is the current value held by the variable.
		 """
		self.name = name
		self.value = None
		self.domain = domain

	def evaluate(self):
		""" Returns the value of a variable. """
		return self.value

class Domain:
	""" This class represents a list pf possible values for 
	a variable, together with the flags. Flags are "new" when the 
	value is available and "X" when it is removed from the domain """

	def __init__(self, values):
		""" Domain constructor. Takes a list of possible values,
		marks them all as available. """
		self.values = values
		self.flags = ["new" for i in range(len(values))] 

def createDomainFromRange(minValue, maxValue):
	""" Creates a Domain by taking minimum and maximum interval values.
	:param minValue: first value of the future domain
	:param maxValue: first not included value of domain.
	e.g. for minValue = 1 and maxValue = 4 the list of
	variables would be [1, 2, 3]. """
	return Domain(range(minValue, maxValue))

class Constraint: # not needed, abstract
	""" An (abstract - not actually used in current implementation)
	 class of a binary constraint. """

	def __init__(self, variable, allowedDomain):
		""" A constraint constructor. Bounds a variable by a domain. 
		:param variable: the constrained variable
		:param allowedDomain: what values are available for the variable"""
		self.variable = variable
		self.allowedDomain = allowedDomain

	def isSatisfied(self):
		""" Checks if a constraint is satisfied.
		Is implemented in subclasses. """
		pass

def findVarName(expression):
	""" Finds a variable in an expression and returns its name. 
	In an expression, variable is always on the left hand side. """
	if isinstance(expression.left, Variable):
		return expression.left.name
	else:
		if isinstance(expression.left, Expression):
			return findVarName(expression.left)
		else:
			return None

def createExpressionFromVar(variable):
	""" Creates a unary exporession from a variable.
	:param variable: variable in the expression. """
	return Expression(variable, None, None)

class Expression(): 
	""" This class represents an expression of a type x + i.
	The variable in the expression is always on the left.
	The expression may not have a right hand side. 
	The expression may also consist of a number, in which case 
	it is written on the left. There is at most one variable 
	in an expression. (This is basically one side of a constraint)
	e.g. x + 2"""

	def __init__(self, left, right, op):
		""" The expression constructor.
		:param left: left hand side of the expression.
		Can be an expression, a variable, or a number.
		:param right: right hand side of the expression.
		Can be a variable or a number.
		:param op: operator (any binary operator) """
		if isinstance(left, Variable):
			self.name = left.name
		else:
			self.name = str(left)
		if right is not None:
			self.name += get_op_string(op)
			if isinstance(right, Variable):
				self.name += right.name
			else:
				self.name += str(right)
		self.left = left
		self.right = right
		self.op = op

	def evaluate(self):
		""" Returns result of an expression.
		This should only be used for expressions where all
		variables have values. """
		if isinstance(self.left, Expression) or isinstance(self.left, Variable):
			lhs = self.left.evaluate()
		else:
			lhs = self.left
		if self.right is None:
			return lhs

		if isinstance(self.right, Expression) or isinstance(self.right, Variable):
			rhs = self.right.evaluate()
		else:
			rhs = self.right
		return self.op(lhs, rhs)

	def substitute(self, value):
		""" Substitutes a value in the variable and returns the result
		of the expression.
		:param value: what value to substitute """
		res = None
		if self.right is None:
			# the expression is of type x
			res = value 
		else:
			# right is digit, e.g. x + 2
			res = self.op(value, self.right)
		return res

class ExpressionConstraint(Constraint):
	""" This class represents a binary constraint which has 
	expressions on either of its sides. """

	def __init__(self, lhs, rhs, op):
		""" Expression constraint constructor. 
		:param lhs: left hand side expression or a variable 
		:param rhs: right hand side expression or a variable
		:param op: the operator of the constraint 
		(e.g. equals, not equals, less than etc.) """
		self.lhs = lhs
		self.rhs = rhs
		self.op = op

	def isSatisfied(self):
		""" Checks if the constraint is satisfied. """
		return self.op(self.lhs.evaluate(), self.rhs.evaluate())

	def valuesSatisfy(self, value1, value2):
		""" Substitutes values in an expression with given values 
		for both sides and returns a check results.
		:param value1: value on the left
		:param value2: value on the right
		 """
		if isinstance(self.lhs, Variable):
			lvalue = value1
		else:
			# it's an expression
			lvalue = self.lhs.substitute(value1)

		if isinstance(self.rhs, Variable):
			rvalue = value2
		else:
			# it's an expression
			rvalue = self.rhs.substitute(value2)
		return self.op(lvalue, rvalue)


class AllDiffConstraint(Constraint):
	""" An "all different" constraint. """
	def __init__(self, variables):
		""" Class constructor.
		:param variables: variables which have to be 
		different to each other """
		self.variables = variables

	def isSatisfied(self):
		""" Checks if all values of all variables are different """
		# this is not used, the method below is used
		valueSet = set([var.value for var in self.variables])
		return len(self.variables) == len(valueSet)

	def to_binary(self):
		""" Converts this constraint to a set of binary constraints.
		This is necessary to use the forward checking algorithm.
		Returns a list of binary constraints """
		constraints = []
		for index in range(len(self.variables) - 1):
			for second_index in range(index + 1, len(self.variables)):
				constraints.append(ExpressionConstraint(createExpressionFromVar(self.variables[index]), createExpressionFromVar(self.variables[second_index]), operator.__ne__))
				constraints.append(ExpressionConstraint(createExpressionFromVar(self.variables[second_index]), createExpressionFromVar(self.variables[index]), operator.__ne__))
		return constraints

class OptimisationConstraint(Constraint):
	""" Optimisation Constraint, where there is a goal 
	to minimise or maximise a parameter. """

	def __init__(self, variable, option):
		""" Constructor. 
		:param variable: the constrained variable 
		:param option: minimise or maximise the variable"""
		self.variable = variable
		self.option = option # option is minimising / maximising

	def getK(self):
		# should find a suitable K for the problem
		# 1. find a solution
		# 2. record k for that solution
		# 3. k +- 1 every time until no solution?
		pass

	def to_binary(self):
		""" Converts an optimisation constraint to a binary one. """
		k = self.getK()
		if self.option == "min":
			op = operator.__lt__
		else:
			op = operator.__gt__
		valueVar = Variable(str(k), Domain([k]))
		return ExpressionConstraint(createExpressionFromVar(self.variable), createExpressionFromVar(valueVar), op)
		pass

class Problem:
	""" Class represents a constraint problem.
	Problem is defined given a set of variables with their domains,
	and a set of constraints. """

	def __init__(self, variables, constraints):
		""" Class constructor. 
		:param variables: a list of variables
		:param constraints: problem constraints """
		self.variables = variables
		self.constraints = constraints
		# self.print_info()

	def print_info(self):
		""" Prints information about the problem """
		print "Problem: ~~~~~~~~~~~~~~~~~"
		print "FIND"
		for variable in self.variables:
			print variable.name,
			print variable.domain.values 
		print "SUCH THAT"
		for constraint in self.constraints:
			print_constraint(constraint)
		print "~~~~~~~~~~~~~~~~~~~~~~~~~~"

def print_constraint(constraint):
	""" Prints information about a constraint.
	e.g. x + 2 < y """
	print constraint.lhs.name + get_op_string(constraint.op) + constraint.rhs.name

def get_op_string(op):
	""" Converts an operator to string for printing purposes. """
	if op is None:
		return " "
	options = {
		   operator.__eq__ : " = ",
		   operator.__ne__ : " != ",
		   operator.__lt__ : " < ",
		   operator.__le__ : " <= ",
		   operator.__gt__ : " > ",
		   operator.__ge__ : " >= ",
		   operator.__add__ : " + ",
		   operator.__mul__ : " * ",
		   operator.__div__ : " / ",
		   operator.__sub__ : " - ",
	}
	return options[op]