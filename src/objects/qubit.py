from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src import constants as const


class Qubit:

    def __init__(self, id, state):
        assert dirac.is_ket(state) and dirac.is_unit(state) and state.size == 2:
        
        self.id = id
        self.state = state
        self.vector_space = state.size

    
    def randomize(self):
        self.state = Ket(np.random.rand(self.vector_space))
    