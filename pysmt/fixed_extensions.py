from pysmt.shortcuts import (Symbol, SBV, Ite, And, Or, BVXor, BVZero, BVSGT, \
                             BVAnd, BV, Not, BVSGE, BVSLE, BVSLT, BVSExt, \
                             BVExtract, BVSGE, BVUGT, Equals, BVZExt)
from pysmt.typing import BVType
import re

def fzero(man_bits):
    return BVZero(man_bits+1)

# Only [-1...1] for now...
def FSymbol(name, man_bits):
    return Symbol(name, BVType(man_bits+1))

def FConst(d, man_bits):
    assert (d < 1 and d >= -1), "{} is out of range".format(d)
    temp = int(d*2**man_bits + (-0.5 if d < 0 else 0.5))
    return SBV(temp, man_bits+1)

def raw_fix_max(man_width):
    return SBV(2**(man_width-1)-1, man_width)

def fix_max(man_width):
    return raw_fix_max(man_width+1)

def raw_fix_min(man_width):
    return SBV(~(2**(man_width-1)-1), man_width)

def fix_min(man_width):
    return raw_fix_min(man_width+1)

def FPlus(*args):
    args = [arg for arg in args]
    if len(args) == 0:
        raise "Too few args for plus"
    a = args[0]
    for b in args[1:]:
        temp = a + b
        width = a.bv_width()
        a = Ite(And(Equals(BVExtract(a, width-1), BVExtract(b, width-1)),
                    Not(Equals(BVExtract(a, width-1), BVExtract(temp, width-1)))),
                Ite(BVSGE(a, BVZero(a.bv_width())),
                    raw_fix_max(a.bv_width()), raw_fix_min(a.bv_width())),
                temp)
        
    return a

def FSub(a,b):
    res = a-b
    width = a.bv_width()
    return Ite(And(Not(Equals(BVExtract(a, width-1), BVExtract(b, width-1))),
                   Not(Equals(BVExtract(a, width-1), BVExtract(res, width-1)))),
               Ite(BVSGE(a, BVZero(a.bv_width())),
                   raw_fix_max(a.bv_width()), raw_fix_min(a.bv_width())),
               res)

def FMul(a, b):
    width = a.bv_width()
    # Double bitwidth
    x, y = BVSExt(a, width), BVSExt(b, width)
    product = x * y
    product = Ite(BVSLT(product, BVZero(2*width)),
                  product - BV(1, 2*width),
                  product)
    ovrflow = BVExtract(product, width-2, width-2)
    product = BVExtract(product, width-1, 2*width-2)
    product = product + BVZExt(ovrflow, width-1)
    return product
                  


def Relu(x):
    width = x.bv_width()
    return Ite(BVSLT(x, BVZero(width)),
               BVZero(width),
               x)

def FGT(a, b):
    return BVSGT(a, b)

def FLT(a, b):
    return BVSLT(a, b)

def FGE(a, b):
    return BVSGE(a, b)

def FLE(a, b):
    return BVSLE(a, b)

def FEQ(a,b):
    return And(BVSGE(a, b), BVSLE(a, b))

def FNE(a,b):
    return Or(BVSLT(a, b), BVSGT(a, b))

def flt_fixed(s):
    match = re.search(r"(\d+)_(\d+)", str(s))
    
    if match:
        exp = int(match.group(2)) - 1
        multiplier = 2**exp
        man = int(match.group(1))
        if man >= multiplier:
            man = -multiplier + (man - multiplier)
        res = float(man)/float(multiplier)
        return str(res)
    return s

def fixed_to_float(s):
    match = re.search(r"(\d+)_(\d+)", str(s))
    if match:
        exp = int(match.group(2)) - 1
        multiplier = 2**exp
        man = int(match.group(1))
        if man >= multiplier:
            man = -multiplier + (man - multiplier)
        res = float(man)/float(multiplier)
        return "{}_f{}".format(res, exp)
    return s

def bv_to_float(s):
    match = re.search(r"\((\w+), (\d+)_(\d+)\)", str(s))
    if match:
        exp = int(match.group(3)) - 1
        multiplier = 2**exp
        man = int(match.group(2))
        if man >= multiplier:
            man = -multiplier + (man - multiplier)
        res = float(man)/float(multiplier)
        return "({}, {}_f{})".format(match.group(1), res, int(match.group(3)))
    return s
