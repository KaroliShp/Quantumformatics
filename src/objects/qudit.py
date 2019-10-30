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

        self._children_systems = None
    

    @property
    def children_systems(self):
        return self._children_systems


    @children_systems.setter
    def children_systems(self, systems: list) -> None:
        if self.system_type == SystemType.simple:
            self._children_systems = systems
            self.system_type = SystemType.product  # Automatically infer
        elif systems is None:
            self._children_systems = None
            self.system_type = SystemType.simple
        else:
            raise ValueError('Quantum system already has children states')
    

    