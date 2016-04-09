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

	c1 = BinaryConstraint(v1, v2, operator.__lt__)
	c2 = BinaryConstraint(v2, v1, operator.__gt__)
	c3 = BinaryConstraint(v2, v3, operator.__ne__)
	c4 = BinaryConstraint(v3, v2, operator.__ne__)

	exp1 = Expression(v2, operator.__add__, 1) # v1 + 1
	exp2 = Expression(v1, None, None)
	ec = ExpressionConstraint(exp1, exp2, operator.__eq__) # v1 + 1 = v2
	ec2 = ExpressionConstraint(exp2, exp1, operator.__eq__) # v2 = v1 + 1


	variables=[v1, v2]
	constraints=[ec, ec2]
	problem = Problem(variables, constraints)
	
	solver = Solver(problem)
	solver.forwardCheck(0)

