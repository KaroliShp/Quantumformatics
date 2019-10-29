from src.dirac_notation.ket import Ket
from src.dirac_notation.bra import Bra
from src.dirac_notation.matrix import Matrix


# Constants for tests


ket_0 = Ket([1, 0])
ket_1 = Ket([0, 1])

ket_00 = Ket([1, 0, 0, 0])
ket_01 = Ket([0, 1, 0, 0])
ket_10 = Ket([0, 0, 1, 0])
ket_11 = Ket([0, 0, 0, 1])

ket_0000 = Ket([1, 0, 0, 0, 0, 0, 0, 0])

bra_0 = Bra([1, 0])
bra_1 = Bra([0, 1])

identity_matrix = Matrix([[1, 0], [0, 1]])
zero_matrix = Matrix([[0, 0], [0, 0]])
pauli_x_matrix = Matrix([[0, 1],[1, 0]])
