import operator

class Variable:
    
    def __init__(self, name, value, domain):
        self.name = name
        self.value = value
        self.domain = domain

    def belongs(self, domain):
    	if domain.values is none:
    		return self.value >= domain.minValue and self.value <= domain.maxValue
    	else:
    		return self.value in domain.values

class Domain:

	def __init__(self, minValue, maxValue):
		self.minValue = minValue
		self.maxValue = maxValue

	def __init__(self, values):
		self.values = values

class Constraint:

	def __init__(self, variable, allowedDomain):
		self.variable = variable
		self.allowedDomain = allowedDomain

	def isSatisfied(self):
		return variable.belongs(allowedDomain)


class ExpressionConstraint(Constraint):
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


class Model:
	def __init__(self, variables):
		self.variables = variables

class Problem:
	def __init__(self, model, constraints):
		self.model = model
		self.constraints = constraints