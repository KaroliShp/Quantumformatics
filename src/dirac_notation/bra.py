import numpy as np

from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation.vector import Vector


class Bra(Vector):
    """
    Class representing row vectors ()
    """

    def __init__(self, obj):
        """
        :param obj: Ket to be transformed into Bra / np.ndarray 1D column vector of shape (1,) / List representing 1D column vector
        """
        if type(obj) == Ket:
            self.vector = np.conj(obj.vector)
        else:
            return super().__init__(obj)

    
    def __str__(self):
        """
        Human readable string representation of a Ket
        """
        sign = lambda x : '-' if x < 0 else '+'

        dirac_str = ''

        for i, component in enumerate(self.vector):
            dirac_str += f'+ ({sign(component.real)} {abs(component.real)} {sign(component.imag)} {abs(component.imag)}i) <{i}| '

        if dirac_str[0] == '+':
            return dirac_str[2:-1]
        else:
            return dirac_str[:-1]


    def __mul__(self, obj):
        """
        Multiplication operator overload (self * obj)
        :param obj: Other object
        :return: Resulting Ket/scalar value/Matrix
        """
        if type(obj) == Ket:
            return np.dot(self.vector, obj.vector)
        elif type(obj) == Matrix:
            return Bra(np.matmul(obj.matrix, self.vector))
        else:
            return super().__mul__(obj)


    def __rmul__(self, obj):
        """
        Reverse multiplication operator overload (obj * self)
        :param obj: Other object
        :return: Resulting Ket/scalar value
        """
        if type(obj) == Ket:
            return Matrix(obj.vector, self.vector)
        else:
            return super().__rmul__(obj)


# bra_0 = bra([1, 0])
# bra_1 = bra([1, 1])
# bra_+ = 1/sqrt(2) * (bra_0 + bra_1)
# bra_- = 1/sqrt(2) * (bra_0 - bra_1)