import pytest
from pytest_mock import mocker
from hamcrest import *
import numpy as np

from src.objects.qudit import Qudit
from src.objects.qubit import Qubit
from src.objects.gate import Gate, GateType
from src.objects.basis import Basis
from src.objects.quantum_system import QuantumSystem, SystemType
from src.actions.actions import *
from src.dirac_notation.constants import *
from src.dirac_notation import functions as dirac

# Test quantum systems


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        Qubit(ket_0), Qubit(ket_1), comp_ket_x(1, 4)
    ), (
        Qudit(comp_ket_x(0, 4)), Qubit(ket_0), comp_ket_x(0, 8)
    )
])
def test_create_composite_system(input_1, input_2, expected_output):
    output = create_composite_system(input_1, input_2)
    
    assert_that(output.state, equal_to(expected_output))
    assert_that(output.children_systems, has_items(input_1, input_2))
    assert_that(output.system_type, equal_to(SystemType.product))


# Reversable processes


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        Gate(identity_matrix(2)), Qubit(ket_0), ket_0
    ), (
        Gate(identity_matrix(4)), Qudit(comp_ket_x(0, 4)), comp_ket_x(0, 4)
    )
])
def test_apply_simple_gate(input_1, input_2, expected_output):
    apply_simple_gate(input_1, input_2)
    
    assert_that(input_2.state, equal_to(expected_output))
    assert_that(input_2.system_type, equal_to(SystemType.simple))
    assert_that(input_2.vector_space, equal_to(expected_output.vector_space))


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        [identity_matrix(2), pauli_x_matrix], [ket_0, ket_0], []
    ),
])
def test_apply_product_gate(input_1, input_2, expected_output):
    product_gate = Gate(dirac.tensor(*input_1))
    product_gate.decomposition = [Gate(matrix) for matrix in input_1]
    
    qudits = [Qubit(state) if state.vector_space == 2 else Qudit(state) for state in input_2]
    composite_system = Qudit(dirac.tensor(*input_2))
    composite_system.children_systems = qudits
    for qudit in qudits:
        qudit.parent_system = composite_system
    
    apply_product_gate(product_gate, composite_system)


