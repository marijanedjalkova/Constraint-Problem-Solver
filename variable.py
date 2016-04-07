class Variable:
    
    def __init__(self, name, value, domain):
        self.name = name
        self.value = value
        self.domain = domain

class Domain:

	def __init__(self, minValue, maxValue):
		self.minValue = minValue
		self.maxValue = maxValue

class Constraint:

	def __init__(self, variable, neededValue, operator):
		self.variable = variable
		self.neededValue = neededValue
		self.operator = operator

class Model:
	def __init__(self, variables):
		self.variables = variables

class Problem:
	def __init__(self, model, constraints):
		self.model = model
		self.constraints = constraints