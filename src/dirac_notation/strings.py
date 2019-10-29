import builtins
"""

do this later

from typing import Union

import numpy as np

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src.dirac_notation import constants as const 


def get_vector_name(obj: Ket):
    # Computational 2D
    try:
        return f'{const.comp_2d_basis_vectors.index(obj)}'
    except ValueError as e:
        pass

    # Fourier 2D
    try:
        return f'{const.four}'


# Specific functions


def parse_bra_ket(obj: Union[Ket,Bra], objs: list = None, precision: int = 2) -> builtins.str:
    view = ''

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
        return view[2:-1]
    else:
        return view[:-1]


# General functions


def str(obj: Union[Ket,Bra,Matrix], objs: list = None, precision: int = 2, info: bool = True) -> builtins.str:
    # Print Bra and Ket as a linear combination of the chosen vectors
    if is_bra(obj) or is_ket(obj):
        view = parse_bra_ket(obj, objs, precision)
        if info:
            return f'value = {view} ; vector space = C^{obj.matrix.shape[0]} ; length = {np.around(np.linalg.norm(obj.matrix), decimals=precision)}'
        else:
            return view

    else:
        return builtins.str(obj)


def print(obj, objs = None, precision = 2, info = True):
    builtins.print(str(obj, objs, precision, info))

"""