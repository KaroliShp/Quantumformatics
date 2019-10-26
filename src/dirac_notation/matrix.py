import numpy as np


class Matrix:
    """
    Class representing a matrix in Dirac notation
    """

    def __init__(self, obj):
        if type(obj) == np.ndarray and len(obj.shape) == 2:
            self.matrix = obj
        else:
            raise ValueError('')


    def __init__(self, ket_vector, bra_vector):
        if type(ket_vector) == np.ndarray and len(ket_vector.shape) == 1 and type(bra_vector) == np.ndarray and len(bra_vector.shape) == 1:
            self.matrix = np.multiply(ket_vector.reshape(ket_vector.shape[0],1), bra_vector)
        else:
            raise ValueError('')

    
    def __str__(self):
        matrix_str = ''
        
        for row in self.matrix:
            matrix_str += f'{row}\n'
        
        return matrix_str[:-1]