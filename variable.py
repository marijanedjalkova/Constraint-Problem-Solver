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


class BinaryConstraint(Constraint):
	def __init__(self, variable1, variable2, op):
		self.variable1 = variable1
		self.variable2 = variable2
		self.op = op

	def isSatisfied(self):
		return self.op(self.variable1.value, self.variable2.value)

	def valuesSatisfy(self, value1, value2):
		return self.op(value1, value2)

class AllDiffConstraint(Constraint):
	def __init__(self, variables):
		self.variables = variables

	def isSatisfied(self):
		valueSet = set([var.value for var in self.variables])
		return len(self.variables) == len(valueSet)

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
	print constraint.variable1.name + get_op_string(constraint.op) + constraint.variable2.name

def get_op_string(op):
	options = {
		   operator.__eq__ : " = ",
           operator.__ne__ : " != ",
           operator.__lt__ : " < ",
           operator.__le__ : " <= ",
           operator.__gt__ : " > ",
           operator.__ge__ : " >= ",
	}
	return options[op]