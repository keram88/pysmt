from pysmt.typing import FixedType
from pysmt.shortcuts import Symbol

def binop_test(operation):
    a,b = Symbol('a', FixedType(0, 4)), Symbol('b', FixedType(0,4))
    
    c = operation(a,b)
    print(c)
binop_test(lambda a,b: a + b)
binop_test(lambda a,b: a - b)
binop_test(lambda a,b: a * b)
binop_test(lambda a,b: a > b)
binop_test(lambda a,b: a >= b)
binop_test(lambda a,b: a < b)
binop_test(lambda a,b: a <= b)
binop_test(lambda a,b: a == b)
