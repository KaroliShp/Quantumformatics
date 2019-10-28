from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src.dirac_notation import constants as const


class Qudit:

    def __init__(self, state: Ket):
        assert dirac.is_ket(state) and dirac.is_unit(state)
        
        self.state = state
        self.vector_space = state.vector_space
        self.composite_system = None
        self.is_entangled = False
    