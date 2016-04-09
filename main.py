from variable import *
from solver import *
import operator

if __name__ == '__main__':
	d1 = createDomainFromRange(3, 6)
	print d1.values
	d2 = createDomainFromRange(2, 4)
	print d2.values
	v1 = Variable("v1", d1)
	v2 = Variable("v2", d2)
	c1 = BinaryConstraint(v1, v2, operator.__eq__)
	c2 = BinaryConstraint(v2, v1, operator.__eq__)
	variables=[v1, v2]
	constraints=[c1, c2]
	problem = Problem(variables, constraints)
	solver = Solver(problem)
	solver.forwardCheck(0)

