from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src.dirac_notation import constants as const

from src.objects.quantum_system import QuantumSystem, SystemType


class Qudit(QuantumSystem):
    """
    General n-dimensional quantum system
    Composition pattern: Composite
    """

    def __init__(self, state: Ket):
        super().__init__(state)

        assert state.vector_space > 2
        self._children_systems = []


    @property
    def children_systems(self):
        return self._children_systems


    @children_systems.setter
    def children_systems(self, systems):
        """
        Simplification - can only belong to one composite system at the moment
        """
        if self._children_systems == []:
            self._children_systems = systems
            self.system_type = SystemType.product
        else:
            raise ValueError('Quantum system already belongs to a composite system')
        
    

    