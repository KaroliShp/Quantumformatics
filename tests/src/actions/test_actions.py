import pytest
from pytest_mock import mocker
from hamcrest import *
import numpy as np

from src.objects.qudit import Qudit
from src.objects.qubit import Qubit
from src.objects.gate import Gate, GateType, cnot_function
from src.objects.basis import Basis
from src.objects.quantum_system import QuantumSystem, SystemType
from src.actions.actions import *
from src.dirac_notation.constants import *
from src.dirac_notation import functions as dirac


# Test are not proper unit tests since no mocks etc. are used
# Gotta fix it later


# Test quantum systems


@pytest.mark.parametrize('input,expected_output', [
    (
        [Qubit(ket_0), Qubit(ket_1)], comp_ket_x(1, 4)
    ), (
        [Qudit(comp_ket_x(0, 4)), Qubit(ket_0)], comp_ket_x(0, 8)
    ), (
        [Qubit(ket_0), Qubit(ket_0), Qubit(ket_0)], comp_ket_x(0, 8)
    )
])
def test_create_composite_system(input, expected_output):
    output = create_composite_system(*input)
    
    assert_that(output.state, equal_to(expected_output))
    assert_that(output.children_systems, has_items(*input))
    assert_that(output.system_type, equal_to(SystemType.product))


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        ket_phi_plus, [Qubit(ket_0), Qubit(ket_1)], SystemType.simple
    )
])
def test_create_entangled_system(input_1, input_2, expected_output):
    output = create_entangled_system(input_1, *input_2)
    
    assert_that(output.state, equal_to(input_1))
    assert_that(output.children_systems, has_items(*input_2))
    assert_that(input_2[0].system_type, equal_to(expected_output))
    assert_that(input_2[1].system_type, equal_to(expected_output))
    assert_that(input_2[0].parent_system, equal_to(output))
    assert_that(input_2[1].parent_system, equal_to(output))
    assert_that(output.system_type, equal_to(SystemType.entangled))


# Reversable processes


@pytest.mark.parametrize('input,expected_output', [
    (
        [Gate(identity_matrix(2)), Gate(identity_matrix(2))], dirac.tensor(identity_matrix(2), identity_matrix(2))
    )
])
def test_create_product_gate(input,expected_output):
    output = create_product_gate(*input)
    
    assert_that(output.gate_type, equal_to(GateType.product))
    assert_that(output.matrix, equal_to(expected_output))
    assert_that(output.decomposition, has_items(*input))


@pytest.mark.parametrize('input,expected_output', [
    (
        [
            Qubit(ket_0), Qubit(ket_0)
        ], [
            dirac.tensor(ket_0, ket_0), ket_0, ket_0, SystemType.product
        ]
    ), (
        [
            Qubit(ket_plus), Qubit(ket_0)
        ], [
            ket_phi_plus, None, None, SystemType.entangled
        ]
    )
])
def test_apply_cnot_gate(input, expected_output):
    # Create CNOT gate
    cnot_gate = Gate(cnot_matrix)
    cnot_gate.gate_type = GateType.interaction
    cnot_gate.interact = cnot_function

    # Create composite system
    composite_system = create_composite_system(*input)
    apply_interaction_gate(cnot_gate, composite_system)
    
    assert_that(composite_system.state, equal_to(expected_output[0]))
    assert_that(input[0].state, equal_to(expected_output[1]))
    assert_that(input[1].state, equal_to(expected_output[2]))
    assert_that(composite_system.system_type, equal_to(expected_output[3]))


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        [
            Gate(identity_matrix(2)), Gate(pauli_x_matrix)
        ], [
            Qubit(ket_0), Qubit(ket_0)
        ], [
            dirac.tensor(identity_matrix(2) * ket_0, pauli_x_matrix * ket_0),
            SystemType.simple, SystemType.simple
        ]
    ), (
        [
            create_product_gate(Gate(identity_matrix(2)), Gate(pauli_x_matrix)),
            Gate(identity_matrix(2))
        ], [
            create_composite_system(Qubit(ket_0), Qubit(ket_0)),
            Qubit(ket_0)
        ], [
            dirac.tensor(identity_matrix(2) * ket_0, pauli_x_matrix * ket_0, identity_matrix(2) * ket_0),
            SystemType.product, SystemType.simple
        ]
    )
])
def test_apply_product_gate(input_1, input_2, expected_output):
    product_gate = create_product_gate(*input_1)
    composite_system = create_composite_system(*input_2)

    apply_product_gate(product_gate, composite_system)

    assert_that(composite_system.state, equal_to(expected_output[0]))
    assert_that(composite_system.system_type, equal_to(SystemType.product))
    for i in range(0, len(input_2)):
        assert_that(input_2[i].system_type, equal_to(expected_output[i+1]))


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        Gate(identity_matrix(2)), Qubit(ket_0), ket_0
    ), (
        Gate(identity_matrix(4)), Qudit(comp_ket_x(0, 4)), comp_ket_x(0, 4)
    ) # Dont know if this test case is valid or not
])
def test_apply_simple_gate(input_1, input_2, expected_output):
    apply_simple_gate(input_1, input_2)
    
    assert_that(input_2.state, equal_to(expected_output))
    assert_that(input_2.system_type, equal_to(SystemType.simple))
    assert_that(input_2.vector_space, equal_to(expected_output.vector_space))