import operator

class Variable:
    
    def __init__(self, name, domain):
        self.name = name
        self.value = None
        self.domain = domain

    def evaluate(self):
    	return self.value

class Domain:

	def __init__(self, values):
		self.values = values
		self.flags = ["new" for i in range(len(values))] 

def createDomainFromRange(minValue, maxValue):
	return Domain(range(minValue, maxValue))

class Constraint: # not needed, abstract

	def __init__(self, variable, allowedDomain):
		self.variable = variable
		self.allowedDomain = allowedDomain

	def isSatisfied(self):
		return self.variable.belongs(self.allowedDomain)

def findVarName(expression):
	if isinstance(expression.left, Variable):
		return expression.left.name
	else:
		if isinstance(expression.left, Expression):
			return findVarName(expression.left)
		else:
			return None

def createExpressionFromVar(variable):
	return Expression(variable, None, None)

class Expression(): # can be x + 2, x - y, x, 3
# numbers are always on the right unless an expression is a number

	def __init__(self, left, right, op):
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
		
		res = None
		if self.right is None:
			res = value 
		else:
			# right is digit, x+ 2
			res = self.op(value, self.right)
		# print "substituting " + str(value) + " in " + self.name +  " gives " + str(res)
		return res

class ExpressionConstraint(Constraint):
	def __init__(self, lhs, rhs, op):
		self.lhs = lhs
		self.rhs = rhs
		self.op = op

	def isSatisfied(self):
		return self.op(self.lhs.evaluate(), self.rhs.evaluate())

	def valuesSatisfy(self, value1, value2):
		# have to substitute values in the expression.
		# Both lhs and rhs are either variables or "x+2" type expressions
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
	def __init__(self, variables):
		self.variables = variables

	def isSatisfied(self):
		valueSet = set([var.value for var in self.variables])
		return len(self.variables) == len(valueSet)

	def to_binary(self):
		constraints = []
		for index in range(len(self.variables) - 1):
			for second_index in range(index + 1, len(self.variables)):
				constraints.append(ExpressionConstraint(createExpressionFromVar(self.variables[index]), createExpressionFromVar(self.variables[second_index]), operator.__ne__))
				constraints.append(ExpressionConstraint(createExpressionFromVar(self.variables[second_index]), createExpressionFromVar(self.variables[index]), operator.__ne__))
		return constraints

class OptimisationConstraint(Constraint):
	def __init__(self, variable, option):
		self.variable = variable
		self.option = option # option is boolean for minimising / maximising

	def to_binary(self):
		pass

class Problem:
	def __init__(self, variables, constraints):
		self.variables = variables
		self.constraints = constraints
		# self.print_info()

	def print_info(self):
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
	print constraint.lhs.name + get_op_string(constraint.op) + constraint.rhs.name

def get_op_string(op):
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