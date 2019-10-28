from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src import constants as const


class Qubit(Qudit):

    def __init__(self, state, id = None):
        super().__init__(id, state)
        assert state.vector_space == 2: