from variable import *
from solver import *
import operator

if __name__ == '__main__':
	print "________________________________________________________________"
	d1 = createDomainFromRange(3, 6)
	d2 = createDomainFromRange(2, 4)
	d3 = Domain([2, 7])

	v1 = Variable("v1", d1)
	v2 = Variable("v2", d2)
	v3 = Variable("v3", d3)

	c1 = BinaryConstraint(v1, v2, operator.__eq__)
	c2 = BinaryConstraint(v2, v1, operator.__eq__)
	c3 = BinaryConstraint(v2, v3, operator.__ne__)
	c4 = BinaryConstraint(v3, v2, operator.__ne__)

	variables=[v1, v2, v3]
	constraints=[c1, c2, c3, c4]
	problem = Problem(variables, constraints)
	
	solver = Solver(problem)
	solver.forwardCheck(0)

