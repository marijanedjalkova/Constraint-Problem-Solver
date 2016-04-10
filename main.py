from variable import *
from solver import *
import operator

if __name__ == '__main__':
	print "________________________________________________________________"
	d1 = createDomainFromRange(3, 6)
	d2 = createDomainFromRange(2, 4)
	d3 = Domain([2, 7, 6, 5, 9])

	v1 = Variable("v1", d1)
	v2 = Variable("v2", d2)
	v3 = Variable("v3", d3)

	ev1 = createExpressionFromVar(v1)
	ev2 = createExpressionFromVar(v2)
	ev3 = createExpressionFromVar(v3)

	c1 = ExpressionConstraint(ev1, ev2, operator.__eq__)
	c2 = ExpressionConstraint(ev2, ev1, operator.__eq__)
	c3 = ExpressionConstraint(ev2, ev3, operator.__ne__)
	c4 = ExpressionConstraint(ev3, ev2, operator.__ne__)

	exp1 = Expression(v2, 1, operator.__add__) # v1 + 1
	exp2 = Expression(v1, None, None)
	ec = ExpressionConstraint(exp1, exp2, operator.__eq__) # v1 + 1 = v2
	ec2 = ExpressionConstraint(exp2, exp1, operator.__eq__) # v2 = v1 + 1


	variables=[v1, v2, v3]
	constraints=[c1, c2, c3, c4]
	problem = Problem(variables, constraints)
	
	solver = Solver(problem, 0)
	solver.forwardCheck(0)

