import numbers

import numpy as np

from src.dirac.bra import Bra
from src.dirac.ket import Ket
from src.dirac.matrix import Matrix


"""
Mathematical functions for Dirac notation
"""


def add(obj1, obj2):
    """
    Add Kets, Bras and Matrices
    """
    if type(obj1) != type(obj2) or (not isinstance(obj1, Vector)) and not isinstance(obj1, Matrix)):
        raise ValueError(f'Cannot add type {type(obj1)} to type {type(obj2)}')
    return obj1 + obj2


def subtract(obj1, obj2):
    """
    Subtract Kets, Bras and Matrices
    """
    if type(obj1) != type(obj2) or (not isinstance(obj1, Vector)) and not isinstance(obj1, Matrix)):
        raise ValueError(f'Cannot subtract type {type(obj1)} from type {type(obj2)}')
    return obj1 - obj2



def multiply(obj1, obj2):
    if type(obj1) != Bra or type(obj2) != Ket:
        raise ValueError(f'')
    return obj1 * obj2