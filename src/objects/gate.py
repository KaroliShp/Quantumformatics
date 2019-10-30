import enum

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src.dirac_notation import constants as const

from src.objects.qubit import Qubit


class GateType(enum.Enum):
    simple = 1
    product = 2
    interaction = 3


class Gate:

    def __init__(self, matrix: Matrix):
        #assert dirac.is_unitary(matrix)
        
        self.matrix = matrix
        self.gate_type = GateType.simple
        self._decomposition = None
        self.interaction_function = None
    

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

    
    # Hacky solution to entangling gate problem


    def interact(self, *qubits):
        return NotImplemented


# Interaction gate functions


def cnot_function(qubit_1, qubit_2):
    assert isinstance(qubit_1, Qubit) and isinstance(qubit_2, Qubit)

    if qubit_1.state == const.ket_0 and qubit_2.state in const.comp_basis_vectors(2):
        return (False, (qubit_1.state, qubit_2.state))
    elif qubit_1.state == const.ket_1 and qubit_2.state == const.ket_0:
        return (False, (qubit_1.state, const.ket_1))
    elif qubit_1.state == const.ket_1 and qubit_2.state == const.ket_1:
        return (False, (qubit_1.state, const.ket_0))
    
    elif qubit_1.state == const.ket_plus and qubit_2.state == const.ket_0:
        return (True, const.ket_phi_plus)
    elif qubit_1.state == const.ket_minus and qubit_2.state == const.ket_0:
        return (True, const.ket_phi_minus)
    elif qubit_1.state == const.ket_plus and qubit_2.state == const.ket_1:
        return (True, const.ket_psi_plus)
    elif qubit_1.state == const.ket_minus and qubit_2.state == const.ket_1:
        return (True, const.ket_psi_minus)
    
    else:
        return NotImplemented

