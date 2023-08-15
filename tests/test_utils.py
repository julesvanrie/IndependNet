from independnet.utils import (
    make_non_negative,
)
import numpy as np


class TestMakeNonNegative:
    def test_positive_number(self):
        assert make_non_negative(5) == 5

    def test_negative_number(self):
        assert make_non_negative(-5.0) == 0

    def test_array(self):
        inp = np.array([5, 5.0, -5, -5.0])
        outp = np.array([5, 5.0, 0, 0])
        assert np.allclose(make_non_negative(inp), outp)
