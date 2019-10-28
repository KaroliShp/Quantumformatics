from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src import constants as const


class Qudit:

    def __init__(self, state, id = None):
        assert dirac.is_ket(state) and dirac.is_unit(state)
        
        self.id = id
        self.state = state
        self.vector_space = state.size
    