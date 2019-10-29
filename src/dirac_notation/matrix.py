import numbers

import numpy as np


class Matrix:
    """
    Class representing a matrix in Dirac notation (not vectors)
    """

    def __init__(self, obj):
        if type(obj) == list:
            obj = np.array(obj)
        assert type(obj) == np.ndarray and len(obj.shape) == 2

        self.matrix = obj


    @property
    def vector_space(self):
        return self.matrix.shape[0]

    
    def linear_combination(self, objs):
        # TODO only let the objects to be an ONB for simplicity?
        if not (False in [ isinstance(obj, Matrix) for obj in objs ]):
            try:
                return (True, np.linalg.solve(np.array([obj.matrix for obj in objs]).transpose(), self.matrix))
            except np.linalg.LinAlgError as e:
                return (False, 0)
        return NotImplemented


    # Magic methods


    def __str__(self):
        matrix_str = ''
        
        for row in self.matrix:
            matrix_str += f'{row}\n'
        
        return matrix_str[:-1]


    def __add__(self, obj):
        if type(self) == type(obj) and self.matrix.shape == obj.matrix.shape:
            return type(self)(self.matrix + obj.matrix)
        return NotImplemented


    def __sub__(self, obj):
        if type(self) == type(obj) and self.matrix.shape == obj.matrix.shape:
            return type(self)(self.matrix - obj.matrix)
        return NotImplemented
        

    def __mul__(self, obj):
        if type(self) == Matrix and type(obj) == Matrix:
            return Matrix(np.matmul(self.matrix, obj.matrix))
        elif isinstance(obj, numbers.Number):
            return type(self)(self.matrix * obj)
        return NotImplemented

    
    def __rmul__(self, obj):
        if isinstance(obj, numbers.Number):
            return type(self)(self.matrix * obj)
        return NotImplemented

    
    def __truediv__(self, obj):
        if isinstance(obj, numbers.Number):
            return type(self)(self.matrix / obj)
        return NotImplemented

    
    def __eq__(self, obj):
        if type(self) == type(obj):
            return np.array_equal(self.matrix, obj.matrix)
        else:
            return False


    def __ne__(self, obj):
        return not self.__eq__(obj)