import operator

class Variable:
    
    def __init__(self, name, domain):
        self.name = name
        self.value = None
        self.domain = domain

class Domain:

	def __init__(self, values):
		self.values = values
		self.flags = ["new" for i in range(len(values))]

def createDomainFromRange(minValue, maxValue):
	return Domain(range(minValue, maxValue))

class Constraint:

	def __init__(self, variable, allowedDomain):
		self.variable = variable
		self.allowedDomain = allowedDomain

	def isSatisfied(self):
		return self.variable.belongs(self.allowedDomain)

def findVarName(expression):
	if isinstance(expression.left, Variable):
		return expression.left.name
	else:
		return findVarName(expression.left)

class Expression():

	def __init__(self, left, op, right):
		self.name = left.name + get_op_string(op) + str(right)
		self.left = left
		self.right = right
		self.op = op

	def evaluate(self):
		if isinstance(self.left, Expression):
			lhs = self.left.evaluate()
		else:
			if isinstance(self.left, Variable):
				lhs = self.left.value 
			else:
				lhs = self.left
		if self.right is None:
			return lhs

		if isinstance(self.right, Expression):
			rhs = self.right.evaluate()
		else:
			if isinstance(self.right, Variable):
				rhs = self.right.value 
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
		print self.name + " for variable " + str(value) + "returns " + str(res)
		return res

class ExpressionConstraint(Constraint):
	def __init__(self, lhs, rhs, op):
		self.lhs = lhs
		self.rhs = rhs
		self.op = op

	def isSatisfied(self):
		return self.op(self.lhs.evaluate(), self.rhs.evaluate())

	def valuesSatisfy(self, value1, value2):
		print "TESTING values " + str(value1) + " and " + str(value2)
		print "for constraint " + self.lhs.name + get_op_string(self.op) + self.rhs.name
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
		print "lvalue = " + str(lvalue),
		print ", rvalue = " + str(rvalue) + " op=" + get_op_string(self.op)
		return self.op(lvalue, rvalue)


class BinaryConstraint(ExpressionConstraint):
	def __init__(self, lhs, rhs, op):
		self.lhs = lhs
		self.rhs = rhs
		self.op = op

	def isSatisfied(self):
		return self.op(self.lhs.value, self.rhs.value)

	def valuesSatisfy(self, value1, value2): # irl they are future and present
		return self.op(value1, value2)

class AllDiffConstraint(Constraint):
	def __init__(self, variables):
		self.variables = variables

	def isSatisfied(self):
		valueSet = set([var.value for var in self.variables])
		return len(self.variables) == len(valueSet)

	def to_binary(self):
		constraints = []
		for index in range(len(self.variables) - 1):
			constraints.append(BinaryConstraint(self.variables[index], self.variables[index + 1], operator.__ne__))
			constraints.append(BinaryConstraint(self.variables[index + 1], self.variables[index], operator.__ne__))
		return constraints

class Problem:
	def __init__(self, variables, constraints):
		self.variables = variables
		self.constraints = constraints
		self.print_info()

	def print_info(self):
		print "Problem: ~~~~~~~~~~~~~~~~~"
		print "GIVEN"
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