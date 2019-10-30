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

    def __init__(self, matrix: Matrix):
        #assert dirac.is_unitary(matrix)
        
        self.matrix = matrix
        self._gate_type = GateType.simple
        self._decomposition = None
    
    
    @property
    def gate_type(self) -> GateType:
        return self._gate_type
    

    @gate_type.setter
    def gate_type(self, gate_type: GateType) -> None:
        if gate_type == GateType.entangling:
            self._decomposition = None
        self._gate_type = gate_type
    

    @property
    def decomposition(self) -> list:
        return self._decomposition


    @decomposition.setter
    def decomposition(self, decomposition: list) -> None:
        self._decomposition = decomposition
        self.gate_type = GateType.product  # Automatically infer


    @property
    def vector_space(self) -> int:
        return self.matrix.vector_space