import operator

class Variable:
    
    def __init__(self, name, domain):
        self.name = name
        self.value = None
        self.domain = domain
        self.flag = "new"

class Domain:

	def __init__(self, values):
		self.values = values

def createDomainFromRange(minValue, maxValue):
	return Domain(range(minValue, maxValue))

class Constraint:

	def __init__(self, variable, allowedDomain):
		self.variable = variable
		self.allowedDomain = allowedDomain

	def isSatisfied(self):
		return variable.belongs(allowedDomain)


class BinaryConstraint(Constraint):
	def __init__(self, variable1, variable2, op):
		self.variable1 = variable1
		self.variable2 = variable2
		self.op = op

	def isSatisfied(self):
		return op(variable1.value, variable2.value)

class AllDiffConstraint(Constraint):
	def __init__(self, variables):
		self.variables = variables

	def isSatisfied(self):
		valueSet = set([var.value for var in variables])
		for var in variables:
			valueSet.add(var.value)
		return len(variables) == len(valueSet)

class Problem:
	def __init__(self, variables, constraints):
		self.variables = variables
		self.constraints = constraints