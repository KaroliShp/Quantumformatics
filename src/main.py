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

from src.experiments.polarization import polarization_experiment

def example():
    # Photon polarization example

    # Set up the system
    qubit_A = Qubit(const.ket_0)  # Vertical polarization, |0>
    qubit_B = Qubit(const.ket_1)  # Horizontal polarization, |1>
    computational_basis = Basis([const.ket_0, const.ket_1])  # Polarising filter 1, {|0>, |1>}
    fourier_basis = Basis([const.ket_plus, const.ket_minus]) # Polarising filter 2, {|+>, |->}

    # Check the probabilities of a vertically polarized photon passing
    # through vertical and horizontal filters 
    p_1 = get_probabilities(computational_basis, qubit_A)
    assert p_1[0] == 1  # Vertically polarized photon will pass with probability 1
    assert p_1[1] == 0  # Horizontally polarized photon will never pass filter

    # Check the probabilities of a vertically polarized photon passing
    # through filters at 45 degrees angles
    p_2 = get_probabilities(fourier_basis, qubit_A)
    assert p_2[0] == 0.5  # Vertically polarized photon will pass with probability 1/2
    assert p_2[1] == 0.5  # Vertically polarized photon will pass with probability 1/2

    # Perform measurement on A in computational basis
    # and check that it is indeed in state 0 after the measurement
    measure(computational_basis, qubit_A)
    assert qubit_A.state == const.ket_0

    # Perform measurement on B in fourier basis and print the resulting state of the qubit
    outcome = measure(fourier_basis, qubit_B)
    print(outcome)
    dirac.print(qubit_B.state)


def experiment_example():
    qubit_A = Qubit(const.ket_0)
    computational_basis = Basis([const.ket_0, const.ket_1])
    result = polarization_experiment(qubit_A, computational_basis)
    print('\nPhoton polarization experiment')
    print(f'Qubit initial state: {qubit_A}')
    print(f'Basis: {computational_basis}')
    print(f'Outcome: {result[0]}')
    print(f'Probabilities: {result[1]}')
    print(f'Qubit final state: {qubit_A}\n')

if __name__ == '__main__':
    experiment_example()
    

    