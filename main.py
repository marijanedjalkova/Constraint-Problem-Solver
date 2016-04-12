from variable import *
from solver import *
import operator

def get_square_index(square_index):
	div = square_index / 3 
	mod = square_index % 3 
	return 27 * div + 3 * mod


def mini_sudoku(size):
	variables = [Variable(("v"+str(i)), createDomainFromRange(1, size+1)) for i in range(size*size)]
	constraints = []
	for i in range(size):
		current_row = variables[(i*size):(i*size + size)]
		adc = AllDiffConstraint(current_row)
		constraints.extend(adc.to_binary())
		current_col = variables[i::size]
		adc = AllDiffConstraint(current_col)
		constraints.extend(adc.to_binary())
	square = []	
	for square_row in range(3):
		for square_col in range(3):
			square_new_index = square_row*3 + square_col
			square.append(variables[square_new_index])
	adc = AllDiffConstraint(square)
	# constraints.extend(adc.to_binary())	
	problem = Problem(variables, constraints)
	
	solver = Solver(problem, 0)
	solver.forwardCheck(0)


def sudoku():
	variables = [Variable(("v"+str(i)), createDomainFromRange(1, 10)) for i in range(81)]
	constraints = []
	for i in range(9):
		current_row = variables[(i*9):(i*9 + 9)]
		adc = AllDiffConstraint(current_row)
		constraints.extend(adc.to_binary())
		current_col = variables[i::9]
		adc = AllDiffConstraint(current_col)
		constraints.extend(adc.to_binary())
	for square_index in range(9):
		square = []	
		for square_row in range(3):
			for square_col in range(3):
				square_new_index = get_square_index(square_index)
				square.append(variables[square_new_index+square_col+square_row*9])
		adc = AllDiffConstraint(square)
		constraints.extend(adc.to_binary())	
	problem = Problem(variables, constraints)
	
	solver = Solver(problem, 1, "sudoku")
	solver.forwardCheck(0)


if __name__ == '__main__':
	print "________________________________________________________________"
	#mini_sudoku(4)	
	sudoku()
	"""
	d1 = createDomainFromRange(3, 6)
	d2 = createDomainFromRange(2, 4)
	d3 = Domain([2, 7, 6, 5, 9])

	# v2 = 5 will be expressed as
	# a variable v2 equal to a variable with domain [5]
	# yes, give it a name
	
	v1 = Variable("v1", d1)
	v2 = Variable("v2", d2)
	v3 = Variable("v3", d3)

	adc = AllDiffConstraint([v1, v2, v3])
	constraints = adc.to_binary()

	ev1 = createExpressionFromVar(v1)
	ev2 = createExpressionFromVar(v2)
	ev3 = createExpressionFromVar(v3)

	c1 = ExpressionConstraint(ev1, ev2, operator.__eq__)
	c2 = ExpressionConstraint(ev2, ev1, operator.__eq__)
	c3 = ExpressionConstraint(ev2, ev3, operator.__ne__)
	c4 = ExpressionConstraint(ev3, ev2, operator.__ne__)


	exp1 = Expression(v2, 1, operator.__add__) # v1 + 1
	exp2 = Expression(5, None, None)
	ec = ExpressionConstraint(exp1, exp2, operator.__eq__) # v1 + 1 = v2
	ec2 = ExpressionConstraint(exp2, exp1, operator.__eq__) # v2 = v1 + 1


	variables=[v1, v2, v3]
	#constraints=[ec, ec2]
	problem = Problem(variables, constraints)
	
	solver = Solver(problem, 1)
	solver.forwardCheck(0)
	"""
