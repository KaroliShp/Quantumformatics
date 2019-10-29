import enum

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src.dirac_notation import constants as const


class GateType(enum.Enum):
    simple = 1
    product = 2
    interaction = 3
    entangling = 4


class Gate:

    def __init__(self, matrix: Matrix, type: GateType):
        assert dirac.is_unitary(matrix)
        
        self.matrix = matrix
        self.type = GateType.simple
        self.decomposition = []
    
    @property
    def vector_space(self) -> int:
        return self.state.vector_space