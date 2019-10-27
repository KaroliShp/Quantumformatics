import numbers
import builtins

import numpy as np

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix


"""
Mathematical functions for Dirac notation
"""


# Type functions


isBra = lambda x : type(x) == Bra
isKet = lambda x : type(x) == Ket
isMatrix = lambda x : type(x) == Matrix


# Basic arithmetic operations


def add(obj1, obj2):
    return obj1 + obj2


def subtract(obj1, obj2):
    return obj1 - obj2


def multiply(obj1, obj2):
    return obj1 * obj2


def divide(obj1, obj2):
    return obj1 / obj2


def equals(obj1, obj2):
    return obj1 == obj2


def not_equals(obj1, obj2):
    return obj1 != obj2


# Additional functions


def braket(obj1, obj2):
    if isBra(obj1) and isKet(obj2):
        return obj1 * obj2
    return NotImplemented


def matrix_multiply(obj1, obj2):
    if isMatrix(obj1) and isMatrix(obj2):
        return Matrix(np.multiply(obj1.matrix, obj2.matrix))
    return NotImplemented


def tensor_product(obj1, obj2):
    if isinstance(obj1, Matrix) and isinstance(obj2, Matrix):
        return Matrix(np.kron(obj1.matrix, obj2.matrix, axes=0))
    return NotImplemented


def linear_combination(obj, objs):
    if isinstance(obj, Matrix):
        return obj.linear_combination(objs)
    return NotImplemented


# Readability functions


def view(obj, objs = None, precision = 2):
    """
    Todo: print diagonalization of a matrix using chosen ONBs
    """

    # Print Bra and Ket as a linear combination of the chosen vectors
    if isBra(obj) or isKet(obj):

        # Get linear combination coefficients
        if objs is None:
            objs = [ Ket([1 if y == x else 0 for y in range(0, (obj.matrix).shape[0]) ]) for x in range (0, (obj.matrix).shape[0]) ]
        res = obj.linear_combination(objs)
        if not res[0]:
            return 'Impossible to decompose using provided information'

        # Helper functions
        sign = lambda x : '+' if x >= 0 else '-'
        vec = lambda x, y : f'|{y}>' if isKet(x) else f'<{y}|'

        # Human readable output
        view = ''
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
            return view[2:-1]
        return view[:-1]

    else:
        return str(obj)


def print(obj, objs = None, precision = 2):
    builtins.print(view(obj, objs, precision))