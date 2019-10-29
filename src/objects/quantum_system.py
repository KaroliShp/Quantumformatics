from typing import List
import enum

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src.dirac_notation import constants as const


class SystemType(enum.Enum):
    simple = 1
    product = 2
    entangled = 3


class QuantumSystem:
    """
    Abstract quantum system representing n-dimensional Hilbert (complex vector) space
    Composition pattern: Component
    """

    def __init__(self, state: Ket) -> None:
        assert dirac.is_ket(state) and dirac.is_unit(state)
        
        self.state = state
        self.parent_system = None  # TODO: expand to n systems
    

    @property
    def vector_space(self) -> int:
        return self.state.vector_space

    
    def __str__(self) -> str:
        return dirac.str(self.state)