from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src.dirac_notation import constants as const
from src.objects.qudit import Qudit

class Qubit(Qudit):
    """
    Special case of a qudit in 2D Hilbert space
    """

    def __init__(self, state: Ket):
        super().__init__(state)
        assert state.vector_space == 2