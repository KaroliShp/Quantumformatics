import numpy as np

from src.dirac_notation.matrix import Matrix


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

    
    def __str__(self):
        return str(self.matrix)
    
    
    def __rmul__(self, obj):
        """
        obj * ket
        """
        if type(obj) == Matrix:
            return Ket(np.matmul(obj.matrix, self.matrix))
        return super().__rmul__(obj)