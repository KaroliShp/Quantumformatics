import math

import numpy as np

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src import constants as const
from src.objects.gate import Gate
from src.objects.qubit import Qubit
from src.objects.qudit import Qudit
from src.objects.basis import Basis


# Qudit functions


def set_state(state: Ket, qudit: Qudit) -> None:
    assert isinstance(state, Ket) and isinstance(qudit, Qudit)

    qudit.state = state
    qudit.vector_space = state.size


def randomize(qudit: Qudit) -> None:
    assert isinstance(qudit, Qudit)

    self.state = Ket(np.random.rand(self.vector_space))


# General functions


def apply_gate(gate: Gate, qudit: Qudit) -> None:
    """
    Apply quantum gate representing a reversable process on a qudit
    """
    assert isinstance(gate, Gate) and isinstance(qudit, Qudit)
    assert gate.rank == qudit.vector_space

    qubit.state = gate.matrix * qudit.state


def get_probabilities(basis: Basis, qudit: Qudit) -> list:
    """
    Get probabilities of qudit measurement on the chosen ONB
    """
    assert isinstance(basis, Basis) and isinstance(qudit, Qudit)
    assert basis.rank == qudit.vector_space
    
    # Obtain probabilities and assert the sum of 1
    result = np.zeros(basis.rank)
    for i in range(0, basis.rank):
        result[i] = abs(Bra(basis.vector[i]) * qudit.state) ** 2
    assert math.isclose(sum(result), 1, abs_tol = 0.02)

    # Hacky way to make it sum up to 1 perfectly (fix later)
    if sum(result) > 1.0:
        result[-1] -= sum(result) - 1.0
    elif sum(result) < 1.0:
        result[-1] += 1.0 - sum(result)

    return result


def measure(basis: Basis, qudit: Qudit) -> int:
    """
    Measure qudit on a chosen ONB
    """
    # Obtain probabilities
    result = measure_basis(basis, qudit)

    # Obtain the outcome
    outcome = np.random.choice(result.shape[0], 1, p = result)

    # Change qudit state
    set_state(basis[outcome], qudit)

    return outcome