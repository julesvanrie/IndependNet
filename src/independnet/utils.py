"""Several utility functions

Functions
---------
    make_non_negative
"""
import numpy.typing as npt


def make_non_negative(input: npt.ArrayLike) -> npt.ArrayLike:
    """Returns the input after changing negative values to zero"""
    if isinstance(input, (int, float)):
        output = max(input, 0)
    else:
        output = input.copy()
        output[output<0] = 0
    return output
