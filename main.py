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
	# Generates a sudoku.
	variables = [Variable(("v"+str(i)), createDomainFromRange(1, 10)) for i in range(81)]
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


if __name__ == '__main__':
	print "________________________________________________________________"
	#mini_sudoku(4)	
	sudoku()