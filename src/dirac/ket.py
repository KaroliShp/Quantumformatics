import numpy as np

from src.dirac.matrix import Matrix


class Ket(Matrix):
    """
    Class representing a column vector in Dirac notation
    """

    def __init__(self, obj):
        if type(obj) == np.ndarray and len(obj.shape) == 1:
            self.matrix = obj
        elif type(obj) == list:
            self.matrix = np.array(obj)
        else:
            raise ValueError('')
    

    # Magic methods


    def __str__(self):
        sign = lambda x : '-' if x < 0 else '+'

        dirac_str = ''

        for i, component in enumerate(self.matrix):
            dirac_str += f'+ ({sign(component.real)} {abs(component.real)} {sign(component.imag)} {abs(component.imag)}i) |{i}> '

        if dirac_str[0] == '+':
            return dirac_str[2:-1]
        else:
            return dirac_str[:-1]

    
    def __rmul__(self, obj):
        """
        obj * ket
        """
        if type(obj) == Matrix:
            return Ket(np.matmul(obj.matrix, self.matrix))
        return super().__rmul__(obj)