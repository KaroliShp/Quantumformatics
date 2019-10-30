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

    def __init__(self, state: Ket):
        assert dirac.is_ket(state) and dirac.is_unit(state)
        
        self.state = state
        self.system_type = SystemType.simple  # Type of this system

        self.has_parent_system = False  # Belongs to a composite system or not
        self._parent_system = None


    @property
    def parent_system(self):
        return self._parent_system


    @parent_system.setter
    def parent_system(self, system) -> None:
        """
        Simplification - can only belong to one composite system at the moment
        """
        if not self.has_parent_system:
            self._parent_system = system
            self.has_parent_system = True
        else:
            raise ValueError('Quantum system already belongs to a composite system')
    

    @property
    def vector_space(self) -> int:
        return self.state.vector_space

    
    def __str__(self) -> str:
        return dirac.str(self.state, info=False)


    def __repr__(self) -> str:
        return self.__str__()