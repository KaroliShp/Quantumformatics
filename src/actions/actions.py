import math

import numpy as np

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src import constants as const
from src.objects.gate import Gate
from src.objects.qubit import Qubit
from src.objects.basis import Basis


def apply_gate(gate, qubit):
    assert type(gate) == Gate and type(qubit) == Qubit
    qubit.state = gate.matrix * qubit.state


def measure_basis(basis, qubit):
    assert type(basis) == Basis and type(qubit) == Qubit
    assert basis.rank == qubit.vector_space
    
    # Obtain probabilities
    result = np.zeros(basis.rank)
    for i in range(0, basis.rank):
        result[i] = abs(Bra(basis.vector[i]) * qubit.state) ** 2
    assert math.isclose(sum(result), 1, abs_tol = 0.02)

    # Hacky way to make it sum up to 1 perfectly
    if sum(result) > 1.0:
        result[-1] -= sum(result) - 1.0
    elif sum(result) < 1.0:
        result[-1] += 1.0 - sum(result)

    return result


def change_state(state, qubit):
    assert type(qubit) == Qubit
    qubit.state = state


def perform_measurement(basis, qubit):
    # Obtain probabilities
    result = measure_basis(basis, qubit)

    # Obtain the outcome
    outcome = np.random.choice(result.shape[0], 1, p = result)

    # Change qubit state
    change_state(basis[outcome], qubit)

    return outcome