"""
Definitions of most common types
"""

from hwt.hdl.types.bits import Bits
from hwt.hdl.types.slice import HSlice
from hwt.hdl.types.string import HString
from hwt.hdl.types.float import HFloat


BOOL = Bits(bit_length=1, name="bool")
INT = Bits(bit_length=32, signed=True, name="int",
           strict_sign=False, strict_width=False)
BIT = Bits(bit_length=1)
BIT_N = Bits(bit_length=1, negated=True)
STR = HString()
SLICE = HSlice()
FLOAT64 = HFloat(11, 52, name="float64")