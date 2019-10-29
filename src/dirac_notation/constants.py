import math
import cmath

import numpy as np

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac


# Kets and Bras


# Computational vectors |0>, |1>, ..., |m>
comp_ket_x = lambda x, d : Ket([ 1 if i == x else 0 for i in range(0, d) ]) if d > x else None
comp_bra_x = lambda x, d : Bra([ 1 if i == x else 0 for i in range(0, d) ]) if d > x else None

# Fourier vectors |e0>, |e1>, ..., |en>
fourier_ket_x = lambda x, d : (1 / math.sqrt(d)) * np.sum([ cmath.rect(1, (2 * math.pi * i * x) / d) * comp_ket_x(i, d) for i in range(0, d) ])
fourier_bra_x = lambda x, d : dirac.adjoint(fourier_ket_x(x, d))

# Angle vectors |0, theta> and |1, theta>
angle_ket_0 = lambda theta : (math.cos(theta / 2) * comp_ket_x(0, 2)) + (math.sin(theta / 2) * comp_ket_x(1, 2))
angle_ket_1 = lambda theta : (math.sin(theta / 2) * comp_ket_x(0, 2)) - (math.cos(theta / 2) * comp_ket_x(1, 2))

# Computational vectors in 2D, |0> and |1>
ket_0 = comp_ket_x(0, 2)
ket_1 = comp_ket_x(1, 2)
bra_0 = dirac.adjoint(ket_0)
bra_1 = dirac.adjoint(ket_0)

# Fourier vectors in 2D, |+> and |->
ket_plus = fourier_ket_x(0, 2)
ket_minus = fourier_ket_x(1, 2)
bra_plus = dirac.adjoint(ket_plus)
bra_minus = dirac.adjoint(ket_minus)

# Computational vectors in C^4, |psi_00>, |psi_01>, |psi_10> and |psi_11>
ket_psi_00 = dirac.tensor(ket_0, ket_0)
ket_psi_01 = dirac.tensor(ket_0, ket_1)
ket_psi_10 = dirac.tensor(ket_1, ket_0)
ket_psi_11 = dirac.tensor(ket_1, ket_1)
bra_psi_00 = dirac.adjoint(ket_psi_00)
bra_psi_01 = dirac.adjoint(ket_psi_01)
bra_psi_10 = dirac.adjoint(ket_psi_10)
bra_psi_11 = dirac.adjoint(ket_psi_11)

# Bell vectors, |omega+>, |omega->, |psi+> and |psi->
ket_phi_plus = (1 / math.sqrt(2)) * ((dirac.tensor(ket_0, ket_0)) + (dirac.tensor(ket_1, ket_1)))
ket_phi_minus = (1 / math.sqrt(2)) * ((dirac.tensor(ket_0, ket_0)) - (dirac.tensor(ket_1, ket_1)))
ket_psi_plus = (1 / math.sqrt(2)) * ((dirac.tensor(ket_0, ket_1)) + (dirac.tensor(ket_1, ket_0)))
ket_psi_minus = (1 / math.sqrt(2)) * ((dirac.tensor(ket_0, ket_1)) - (dirac.tensor(ket_1, ket_0)))
bra_phi_plus = dirac.adjoint(ket_phi_plus)
bra_phi_minus = dirac.adjoint(ket_phi_minus)
bra_psi_plus = dirac.adjoint(ket_psi_plus)
bra_psi_minus = dirac.adjoint(ket_psi_minus)


# Unitary matrices


# Basic matrices
zero_matrix = lambda d1, d2 : Matrix(np.zeros((d1, d2)))
identity_matrix = lambda d : Matrix(np.identity(d))

# Pauli matrices
pauli_x_matrix = Matrix(np.array([[0, 1], [1, 0]]))
pauli_y_matrix = Matrix(np.array([[0, -1.0j], [1.0j, 0]]))
pauli_z_matrix = Matrix(np.array([[1, 0], [0, -1]]))
n_sigma_matrix = lambda nx, ny, nz : (nx * pauli_x_matrix) + (ny * pauli_y_matrix) + (nz * pauli_z_matrix)

# Fourier transform matrix
fourier_transform_matrix = lambda d : sum([ fourier_ket_x(i, d) * comp_bra_x(i, d) for i in range(0, d) ], zero_matrix(d, d))
hadamard_matrix = fourier_transform_matrix(2) # 2D is known as Hadamard gate (H)

# CNOT matrix
cnot_matrix = dirac.tensor((ket_0 * bra_0), identity_matrix(2)) + dirac.tensor((ket_1 * bra_1), pauli_x_matrix)