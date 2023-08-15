"""Several utility functions

Functions
---------
    make_non_negative
"""
import numpy.typing as npt


def make_non_negative(inp: npt.ArrayLike) -> npt.ArrayLike:
    """Returns the inp after changing negative values to zero"""
    if isinstance(inp, (int, float)):
        outp = max(inp, 0)
    else:
        outp = inp.copy() # type: ignore
        outp[outp<0] = 0
    return outp
