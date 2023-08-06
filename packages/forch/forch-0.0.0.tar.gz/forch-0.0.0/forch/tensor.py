import numpy as np


class Tensor(object):
    def __init__(self, data, requires_grad: bool = False):
        self._data = np.array(data)
        # Gradient info
        self.grad = None
        self.requires_grad = requires_grad
        # TODO: deal with is_leaf
        # Leaf variable is the variable created by user
        self.is_leaf = False
        # TODO: deal with grad_fn
        self.grad_fn = None

    @property
    def data(self) -> np.ndarray:
        return self._data

    @data.setter
    def data(self, new_data) -> None:
        self._data = np.array(new_data)

    def size(self) -> tuple:
        return self._data.shape

    def requires_grad_(self, new_requires_grad: bool) -> None:
        self.requires_grad = new_requires_grad
