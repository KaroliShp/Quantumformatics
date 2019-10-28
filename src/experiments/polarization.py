import numpy as np

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src.dirac_notation import constants as const

from src.objects.basis import Basis
from src.objects.composition import Composition
from src.objects.gate import Gate
from src.objects.qudit import Qudit
from src.objects.qubit import Qubit
from src.actions.actions import * # todo import properly


def polarization_experiment(qubit: Qubit, basis: Basis) -> tuple:
    probabilities = get_probabilities(basis, qubit)
    outcome = measure(basis, qubit)
    return (outcome, probabilities)