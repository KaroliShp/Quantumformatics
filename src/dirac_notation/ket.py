import numbers

import numpy as np

from src.dirac_notation.matrix import Matrix
from src.dirac_notation.vector import Vector


class Ket(Vector):
    """
    Class representing a column vector in Dirac notation
    """
    
    # Magic methods


    def __str__(self):
        """
        Human readable string representation of a Ket
        """
        sign = lambda x : '-' if x < 0 else '+'

        dirac_str = ''

        for i, component in enumerate(self.vector):
            dirac_str += f'+ ({sign(component.real)} {abs(component.real)} {sign(component.imag)} {abs(component.imag)}i) |{i}> '

        if dirac_str[0] == '+':
            return dirac_str[2:-1]
        else:
            return dirac_str[:-1]

    
    def __rmul__(self, obj):
        """
        Reverse multiplication operator overload (obj * self)
        :param obj: Other object
        :return: Resulting Ket/scalar value
        """
        if type(obj) == Matrix:
            return Ket(np.matmul(obj.matrix, self.vector))
        else:
            return super().__rmul__(obj)


    # Getters/setters


    def get_dimensions(self):
        return self.vector.shape[0]


    def get_coefficients(self):
        return self.vector