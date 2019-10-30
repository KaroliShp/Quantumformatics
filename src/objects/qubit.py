from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src.dirac_notation import constants as const

from src.objects.quantum_system import QuantumSystem, SystemType


class Qubit(QuantumSystem):
    """
    Special case of a qudit in 2D Hilbert space, basic unit
    Composition pattern: Leaf
    """

    def __init__(self, state: Ket):
        super().__init__(state)
        assert state.vector_space == 2