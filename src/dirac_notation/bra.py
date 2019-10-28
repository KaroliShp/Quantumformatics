import numpy as np

from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix


class Bra(Matrix):
    """
    Class representing row vectors in Dirac notation
    """

    def __init__(self, obj):
        if type(obj) == np.ndarray and len(obj.shape) == 1:
            self.matrix = obj
        elif type(obj) == list:
            self.matrix = np.array(obj)
        elif type(obj) == Ket:
            self.matrix = np.conj(obj.matrix)
        else:
            raise ValueError('')
        
        self.vector_space = self.matrix.size

    
    def __str__(self):
        return str(self.matrix)
    

    def __mul__(self, obj):
        """
        Multiplication operator overload (self * obj)
        """
        if type(obj) == Ket:
            return np.dot(self.matrix, obj.matrix)
        elif type(obj) == Matrix:
            return Bra(np.matmul(obj.matrix, self.matrix))
        else:
            return super().__mul__(obj)


    def __rmul__(self, obj):
        """
        Reverse multiplication operator overload (obj * self)
        :param obj: Other object
        :return: Resulting Ket/scalar value
        """
        if type(obj) == Ket:
            return Matrix(np.multiply(obj.matrix.reshape(obj.matrix.shape[0],1), self.matrix))
        else:
            return super().__rmul__(obj)