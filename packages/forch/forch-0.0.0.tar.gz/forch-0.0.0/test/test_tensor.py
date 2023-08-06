import unittest
import numpy as np
from forch.tensor import Tensor


class TestTensor(unittest.TestCase):
    def test_create_from_list(self):
        d1 = [1, 2, 3]
        t1 = Tensor(d1)
        assert t1.size() == (3,)

    def test_create_from_numpy_array(self):
        shape = (4, 5)
        d1 = np.random.rand(*shape)
        t1 = Tensor(d1)
        assert t1.size() == shape
