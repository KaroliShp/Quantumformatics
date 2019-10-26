import numbers

import numpy as np


class Vector:

    def __init__(self, obj):
        """
        :param obj: np.ndarray 1D column vector of shape (1,) / List representing 1D column vector
        """
        if type(obj) == np.ndarray:
            self.vector = obj
        elif type(obj) == list:
            self.vector = np.array(obj)
        else:
            raise ValueError('')
    
    
    # Magic methods


    def __add__(self, vector):
        """
        Addition operator overload (self + vector)
        :param vector: Vector to be added to self
        :return: Resulting Vector of self type
        """
        if type(self) != type(vector):
            raise ValueError(f'Cannot add/subtract {type(self)} to/from {type(vector)}')
        if self.vector.shape[0] != vector.vector.shape[0]:
            raise ValueError(f'Cannot add up vectors of different dimensions ({self.dimensions} and {vector.dimensions})')

        return type(self)(self.vector + vector.vector)
    

    def __sub__(self, vector):
        """
        Subtraction operator overload (self - vector)
        :param vector: Vector to be subtracted from self
        :return: Resulting Vector of self type
        """
        return self.__add__(self, (-1)*vector)

    
    def __mul__(self, scalar):
        """
        Multiplication operator overload (self * scalar)
        :param scalar: Scalar
        :return: Resulting Vector of self type
        """
        if isinstance(scalar, numbers.Number):
            return type(self)(self.vector * scalar)
        else:
            # In case Ket * Bra, this will call Bra.__rmul__() which will calculate the correct value
            return NotImplemented

    
    def __rmul__(self, scalar):
        """
        Reverse multiplication operator overload (obj * self)
        :param obj: Other object
        :return: Resulting Ket/scalar value
        """
        if isinstance(scalar, numbers.Number):
            return type(self)(self.vector * scalar)
        else:
            return NotImplemented

    
    def __truediv__(self, scalar):
        """
        Division operator overload (self / scalar)
        :param scalar: Scalar
        :return: Resulting Vector
        """
        if isinstance(scalar, numbers.Number):
            return type(self)(self.vector / scalar)
        else:
            raise(f'Cannot divide {type(self)} by an object of type {type(scalar)}')

    
    def __eq__(self, vector):
        """
        Equality operator overload (self == vector)
        :param vector: Vector to compare to
        :return: Truth value
        """
        if type(self) == type(vector):
            return np.array_equal(self.vector, vector.vector)
        else:
            raise(f'Cannot compare f{type(self)} with an object of type {type(vector)}')


    def __ne__(self, vector):
        """
        Not equals operator overload (self != vector)
        :param vector: Vector to compare to
        :return: Truth value
        """
        return not self.__eq__(vector)
