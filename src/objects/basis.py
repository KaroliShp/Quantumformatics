import numpy as np

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src.dirac_notation import constants as const


class Basis:

    def __init__(self, states: list):
        # Check that the vectors form an ONB
        # TODO fix assertion tolerance
        states_arr = np.array([state.matrix for state in states])
        assert states_arr.shape[0] == states_arr.shape[1]
        assert np.allclose(states_arr.transpose() * states_arr, const.identity_matrix(states_arr.shape[0]).matrix, atol=0.8)

        self.states = states
        self.vector_space = states_arr.shape[0]
    

    def __str__(self):
        string = '{'
        for state in self.states:
            string += f' {dirac.str(state, info=False)};'
        return f'{string} }}, dimensions = {self.vector_space}'