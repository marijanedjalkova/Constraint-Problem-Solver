from variable import *
from solver import *
import operator

def get_square_index(square_index):
	# this is for sudoku square check
	# returns index of a top left variable for a given square
	# square_index is between 0 and 8
	# sudoku is represented by a list of variables
	# v0-v80 written in rows.
	div = square_index / 3 
	mod = square_index % 3 
	return 27 * div + 3 * mod


def mini_sudoku(size):
	# generates a sudoku of a specified size.
	# a simplified version of sudoku, was used for testing
	# on size 3. 
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
	# Generates a sudoku. No values given at all
	variables = [Variable(("v"+str(i)), createDomainFromRange(1, 10)) for i in range(81)]
	variables[4].domain = Domain([9])
	variables[5].domain = Domain([4])
	variables[10].domain = Domain([7])
	variables[12].domain = Domain([6])
	variables[15].domain = Domain([3])
	variables[21].domain = Domain([1])
	variables[25].domain = Domain([6])
	variables[27].domain = Domain([6])
	variables[28].domain = Domain([4])
	variables[29].domain = Domain([8])
	variables[35].domain = Domain([5])
	variables[36].domain = Domain([9])
	variables[39].domain = Domain([2])
	variables[44].domain = Domain([6])
	variables[47].domain = Domain([2])
	variables[49].domain = Domain([4])
	variables[51].domain = Domain([7])
	variables[52].domain = Domain([9])
	variables[54].domain = Domain([8])
	variables[55].domain = Domain([1])
	variables[57].domain = Domain([4])
	variables[59].domain = Domain([9])
	variables[63].domain = Domain([2])
	variables[65].domain = Domain([5])
	variables[68].domain = Domain([8])
	variables[70].domain = Domain([3])
	variables[73].domain = Domain([6])
	variables[74].domain = Domain([4])
	variables[76].domain = Domain([1])
	variables[77].domain = Domain([3])
	constraints = []
	for i in range(9):
		# add row constraints
		current_row = variables[(i*9):(i*9 + 9)]
		adc = AllDiffConstraint(current_row)
		constraints.extend(adc.to_binary())
		# add column constraints
		current_col = variables[i::9]
		adc = AllDiffConstraint(current_col)
		constraints.extend(adc.to_binary())
	# add square constraints
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
	solver2 = Solver(problem, 1, "sudoku")
	solver2.forwardCheck(0)


if __name__ == '__main__':
	print "________________________________________________________________"
	#mini_sudoku(4)	
	sudoku()