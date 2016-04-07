import operator

class Variable:
    
    def __init__(self, name, value, domain):
        self.name = name
        self.value = value
        self.domain = domain

    def belongs(self, domain):
    	return self.value >= domain.minValue and self.value <= domain.maxValue

class Domain:

	def __init__(self, minValue, maxValue):
		self.minValue = minValue
		self.maxValue = maxValue

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

	def function(op):
	    return {
	        '<' : operator.__lt__,
	        '<=' : operator.__le__,
	        '>' : operator.__gt__,
	        '>=' : operator.__ge__,
	        '==' : operator.__eq__,
	        '!=' : operator.__ne__,
	        }[op]

	def isSatisfied(self):
		return function(op)(variable1.value, variable2.value)


class Model:
	def __init__(self, variables):
		self.variables = variables

class Problem:
	def __init__(self, model, constraints):
		self.model = model
		self.constraints = constraints