import math
import cmath

import numpy as np

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac


# Kets and Bras

# Functions

comp_ket_x = lambda x, d : Ket([ 1 if i == x else 0 for i in range(0, d) ])
comp_bra_x = lambda x, d : Bra([ 1 if i == x else 0 for i in range(0, d) ])

fourier_ket_x = lambda x, d : (1 / math.sqrt(d)) * np.sum([ cmath.rect(1, (2 * math.pi * i * x) / d) * comp_ket_x(i, d) for i in range(0, d) ])
fourier_bra_x = lambda x, d : Bra(fourier_ket_x(x, d))

angle_ket_0 = lambda theta : (math.cos(theta / 2) * comp_ket_x(0, 2)) + (math.sin(theta / 2) * comp_ket_x(1, 2))
angle_ket_1 = lambda theta : (math.sin(theta / 2) * comp_ket_x(0, 2)) - (math.cos(theta / 2) * comp_ket_x(1, 2))

# Constants

ket_0 = comp_ket_x(0, 2)
ket_1 = comp_ket_x(1, 2)
bra_0 = Bra(ket_0)
bra_1 = Bra(ket_0)

ket_plus = fourier_ket_x(0, 2)
ket_minus = fourier_ket_x(1, 2)
bra_plus = Bra(ket_plus)
bra_minus = Bra(ket_minus)

ket_psi_00 = dirac.tensor(ket_0, ket_0)
ket_psi_01 = dirac.tensor(ket_0, ket_1)
ket_psi_10 = dirac.tensor(ket_1, ket_0)
ket_psi_11 = dirac.tensor(ket_1, ket_1)
bra_psi_00 = Bra(ket_psi_00)
bra_psi_01 = Bra(ket_psi_01)
bra_psi_10 = Bra(ket_psi_10)
bra_psi_11 = Bra(ket_psi_11)

ket_phi_plus = (1 / math.sqrt(2)) * ((dirac.tensor(ket_0, ket_0)) + (dirac.tensor(ket_1, ket_1)))
ket_phi_minus = (1 / math.sqrt(2)) * ((dirac.tensor(ket_0, ket_0)) - (dirac.tensor(ket_1, ket_1)))
ket_psi_plus = (1 / math.sqrt(2)) * ((dirac.tensor(ket_0, ket_1)) + (dirac.tensor(ket_1, ket_0)))
ket_psi_minus = (1 / math.sqrt(2)) * ((dirac.tensor(ket_0, ket_1)) - (dirac.tensor(ket_1, ket_0)))
bra_phi_plus = Bra(ket_phi_plus)
bra_phi_minus = Bra(ket_phi_minus)
bra_psi_plus = Bra(ket_psi_plus)
bra_psi_minus = Bra(ket_psi_minus)

#todo ket_ghz

"""
# Basis


comp_basis = lambda d : Basis([ comp_ket_x(i, d) for i in range(0, d) ])
fourier_basis = lambda d : Basis([ fourier_ket_x(i, d) for i in range(0, d) ])
"""

# Unitary matrices

zero_matrix = lambda d1, d2 : Matrix(np.zeros((d1, d2)))
identity_matrix = lambda d : Matrix(np.identity(d))

pauli_x_matrix = Matrix(np.array([[0, 1], [1, 0]])) # Try to write as a linear combination of ONBs?
pauli_y_matrix = Matrix(np.array([[0, -1.0j], [1.0j, 0]]))
pauli_z_matrix = Matrix(np.array([[1, 0], [0, -1]]))
n_sigma_matrix = lambda nx, ny, nz : (nx * pauli_x_matrix) + (ny * pauli_y_matrix) + (nz * pauli_z_matrix)

fourier_transform_matrix = lambda d : sum([ fourier_ket_x(i, d) * comp_bra_x(i, d) for i in range(0, d) ], zero_matrix(d, d))
hadamard_matrix = fourier_transform_matrix(2) # 2D is known as Hadamard gate (H)
#print(hadamard_matrix == (fourier_ket_x(0, 2)*comp_bra_x(0, 2) + fourier_ket_x(1, 2)*comp_bra_x(1, 2)))

cnot_matrix = dirac.tensor((ket_0 * bra_0), identity_matrix(2)) + dirac.tensor((ket_1 * bra_1), pauli_x_matrix)


# Examples

"""
ket_phi_x = (1 / math.sqrt(2)) * ((dirac.tensor(ket_0, ket_0)) + (dirac.tensor(ket_1, ket_1)))
ket_phi_y = (1 / math.sqrt(2)) * (ket_psi_00 + ket_psi_11)

print(ket_phi_x == ket_phi_y)
dirac.print(ket_phi_x, [ket_psi_00, ket_psi_01, ket_psi_10, ket_psi_11])

bra_phi_y = (1 / math.sqrt(2)) * (bra_psi_00 + bra_psi_11)
print(Bra(ket_phi_y) == bra_phi_y)
"""