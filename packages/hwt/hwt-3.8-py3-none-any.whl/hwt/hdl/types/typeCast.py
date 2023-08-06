
from typing import Optional, Any

from hwt.hdl.types.defs import INT, STR, BOOL, SLICE, FLOAT64
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.value import HValue
from hwt.hdl.variables import SignalItem
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase

defaultPyConversions = {
    int: INT,
    str: STR,
    bool: BOOL,
    slice: SLICE,
    float: FLOAT64
}


def toHVal(op: Any, suggestedType: Optional[HdlType]=None):
    """Convert python or hdl value/signal object to hdl value/signal object"""
    if isinstance(op, HValue) or isinstance(op, SignalItem):
        return op
    elif isinstance(op, InterfaceBase):
        return op._sig
    else:
        if suggestedType is not None:
            return suggestedType.from_py(op)

        if isinstance(op, int):
            if op >= 1 << 31:
                raise TypeError(
                    f"Number {op:d} is too big to fit in 32 bit integer of HDL"
                    " use Bits type instead")
            elif op < -(1 << 31):
                raise TypeError(
                    f"Number {op:d} is too small to fit in 32 bit integer"
                    " of HDL use Bits type instead")

        try:
            hType = defaultPyConversions[type(op)]
        except KeyError:
            hType = None

        if hType is None:
            raise TypeError(f"Unknown hardware type for instance of {op.__class__}")

        return hType.from_py(op)
