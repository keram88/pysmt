from pysmt.typing import FixedType
from pysmt.shortcuts import Symbol

def get_args(a_iw, a_mw, b_iw, b_mw):
    return (Symbol('a_{}_{}'.format(a_iw, a_mw), FixedType(a_iw,a_mw)),
            Symbol('b_{}_{}'.format(b_iw, b_mw), FixedType(b_iw,b_mw)))

try:
    a,b = get_args(0,4,0,4)
    a+b
except:
    print("Error")
else:
    print("Success")
    
try:
    a,b = get_args(0,4,0,5)
    a+b
except:
    print("Success")
else:
    print("Error")
    
try:
    a,b = get_args(1,4,0,4)
    a+b
except:
    print("Success")
else:
    print("Error")

try:
    a,b = get_args(1,4,2,4)
    a+b
except:
    print("Success")
else:
    print("Error")

try:
    a,b = get_args(0,1,2,4)
    a+b
except:
    print("Success")
else:
    print("Error")
