import numbers
import builtins
from functools import reduce

import numpy as np

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix


"""
Mathematical functions for Dirac notation
"""


# Type functions


is_bra = lambda x : type(x) == Bra
is_ket = lambda x : type(x) == Ket
is_matrix = lambda x : type(x) == Matrix
is_same = lambda x, y : type(x) == type(y)


# Arithmetic operations


def matrix_mult_elem(obj1, obj2):
    if is_matrix(obj1) and is_matrix(obj2):
        return np.multiply(obj1.matrix, obj2.matrix)
    return NotImplemented


def braket(obj1, obj2):
    if is_bra(obj1) and is_ket(obj2):
        return obj1 * obj2
    return NotImplemented


def tensor(obj1, obj2, *args):
    if isinstance(obj1, Matrix) and isinstance(obj2, Matrix) and is_same(obj1, obj2) and not (False in [is_same(obj1, arg) for arg in args]):
        # TODO could probably improve the performance
        return type(obj1)(reduce(lambda x, y : np.kron(x, y), [obj1.matrix] + [obj2.matrix] + list(map(lambda z: z.matrix, args))))
    return NotImplemented


def linear_combination(obj, objs):
    if isinstance(obj, Matrix):
        return obj.linear_combination(objs)
    return NotImplemented


def adjoint(obj):
    if is_ket(obj):
        return Bra(obj)
    elif is_bra(obj):
        return Ket(np.conj(obj.matrix))
    elif is_matrix(obj):
        return Matrix(np.conj(obj.matrix).transpose())
    return NotImplemented


# Information functions


is_unit = lambda x : (is_bra(x) or is_ket(x)) and np.round(np.linalg.norm(x.matrix), 2) == 1.0
is_unitary = lambda x : is_matrix(x) and np.allclose(np.identity(x.vector_space), (adjoint(x) * x).matrix, atol=0.8)
is_orthogonal = lambda x, y : is_same(x, y) and (is_bra(x) or is_ket(x)) and np.dot(x.matrix, y.matrix) == 0
is_orthonormal = lambda x, y : is_orthogonal(x, y) and is_unit(x) and is_unit(y)


# Readability functions


def str(obj, objs = None, precision = 2, info = True):
    """
    Todo: print diagonalization of a matrix using chosen ONBs
    Extract to be reused throughout
    """

    view = ''

    # Print Bra and Ket as a linear combination of the chosen vectors
    if is_bra(obj) or is_ket(obj):

        # Get linear combination coefficients
        if objs is None:
            objs = [ Ket([1 if y == x else 0 for y in range(0, (obj.matrix).shape[0]) ]) for x in range (0, (obj.matrix).shape[0]) ]
        res = obj.linear_combination(objs)
        if not res[0]:
            return 'Impossible to decompose using provided information'

        # Helper functions
        sign = lambda x : '+' if x >= 0 else '-'
        vec = lambda x, y : f'|{y}>' if is_ket(x) else f'<{y}|'

        # Human readable output
        for i, c in enumerate(res[1]):
            # Printing precision
            c = np.around(c, decimals = precision)

            temp = ''

            # Take care of real part
            if c.real == -1 and c.imag == 0:
                temp += f'- '
            elif c.real == 1 and c.imag == 0:
                pass
            elif c.real != 0:
                temp += f'{sign(c.real)} {abs(c.real)} '
            
            # Take care of imaginary part
            if abs(c.imag) == 1:
                temp += f'{sign(c.imag)}i '
            elif c.imag != 0:
                temp += f'{sign(c.imag)} {abs(c.imag)}i'
            
            # Special case for parentheses
            if temp and c.real != 0 and c.imag != 0 and temp[0] == '+':
                temp = temp[2:]

            # Finalise the term
            if not temp and c.real == 1:
                view += f'+ {vec(objs[i], i)} '                
            elif temp and c.real != 0 and c.imag != 0:
                view += f'+ ({temp}){vec(objs[i], i)} '
            elif temp:
                view += f'{temp} {vec(objs[i], i)} '

        # Take out the leading + if exists and trailing whitespace
        if view[0] == '+':
            view = view[2:-1]
        else:
            view = view[:-1]
        
        # Add more information
        if info:
            return f'value = {view} ; vector space = C^{obj.matrix.shape[0]} ; length = {np.around(np.linalg.norm(obj.matrix), decimals=precision)}'
        else:
            return view

    else:
        return builtins.str(obj)


def print(obj, objs = None, precision = 2, info = True):
    builtins.print(str(obj, objs, precision, info))