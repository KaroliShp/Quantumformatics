import pytest
from pytest_mock import mocker
from hamcrest import *
import numpy as np

from src.objects.gate import Gate, GateType, cnot_function
from src.dirac_notation.constants import *
from src.objects.qubit import Qubit


@pytest.mark.parametrize('input,expected_output', [
    (
        identity_matrix(2), GateType.simple
    ), (
        identity_matrix(4), GateType.simple
    )
])
def test_init(input, expected_output):
    gate= Gate(input)

    assert_that(gate.gate_type, equal_to(expected_output))
    assert_that(gate.decomposition, equal_to(None))

"""
@pytest.mark.parametrize('input', [
    (
        Matrix([[1, 1],[0,0]])
    )
])
def test_init_fail(input):
    try:
        gate = Gate(input)
        pytest.fail()
    except AssertionError:
        pass
"""


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        Qubit(ket_0), Qubit(ket_1), (False, (ket_0, ket_1))
    ), (
        Qubit(ket_1), Qubit(ket_1), (False, (ket_1, ket_0))
    ), (
        Qubit(ket_minus), Qubit(ket_1), (True, ket_psi_minus)
    )
])
def test_cnot_function(input_1, input_2, expected_output):
    output = cnot_function(input_1, input_2)
    assert_that(output[0], equal_to(expected_output[0]))
    assert_that(output[1], equal_to(expected_output[1]))