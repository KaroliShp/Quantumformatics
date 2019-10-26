import math
import cmath

import numpy as np

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation.basis import Basis


# Kets and Bras


comp_ket_x = lambda x, d : Ket([ 1 if i == x else 0 for i in range(0, d) ])
comp_bra_x = lambda x, d : Bra([ 1 if i == x else 0 for i in range(0, d) ])

fourier_ket_x = lambda x, d : (1 / math.sqrt(d)) * np.sum([ cmath.rect(1, (2 * math.pi * i * x) / d) * comp_ket_x(i, d) for i in range(0, d) ])
fourier_bra_x = lambda x, d : Bra(fourier_ket_x(x, d))

angle_ket_0 = lambda theta : (math.cos(theta / 2) * comp_ket_x(0, 2)) + (math.sin(theta / 2) * comp_ket_x(1, 2))
angle_ket_1 = lambda theta : (math.sin(theta / 2) * comp_ket_x(0, 2)) - (math.cos(theta / 2) * comp_ket_x(1, 2))


# Basis


comp_basis = lambda d : Basis([ comp_ket_x(i, d) for i in range(0, d) ])
fourier_basis = lambda d : Basis([ fourier_ket_x(i, d) for i in range(0, d) ])


# Unitary matrices


identity_matrix = Matrix(np.array([1, 0], [0, 1]))

pauli_x_matrix = Matrix(np.array([[0, 1], [1, 0]])) # Try to write as a linear combination of ONBs?
pauli_y_matrix = Matrix(np.array([[0, -1.0j], [1.0j, 0]]))
pauli_z_matrix = Matrix(np.array([[1, 0], [0, -1]]))
n_sigma_matrix = lambda nx, ny, nz : (nx * pauli_x_matrix) + (ny * pauli_y_matrix) + (nz * pauli_z_matrix)

fourier_transform_matrix = lambda d : sum([ fourier_ket_x(i, d) * comp_bra_x(i, d) for i in range(0, d) ])
hadamard_matrix = fourier_transform_matrix(2) # 2D is known as Hadamard gate (H)

