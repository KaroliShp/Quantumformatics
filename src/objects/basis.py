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
        assert np.allclose(states_arr.transpose() * states_arr, const.identity_matrix(states_arr.shape[0]).matrix, atol=1)

        self.states = states
        self.vector_space = states_arr.shape[0]