import pytest
from pytest_mock import mocker
from hamcrest import *
import numpy as np

from src.objects.gate import Gate, GateType
from src.dirac_notation.constants import *


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


@pytest.mark.parametrize('input_1,input_2', [
    (
        identity_matrix(2), GateType.simple
    ), (
        identity_matrix(4), GateType.product
    ), (
        cnot_matrix, GateType.entangling
    )
])
def test_gate_type(input_1, input_2):
    gate = Gate(input_1)
    if input_2 == GateType.entangling:
        gate.decomposition = []
    gate.gate_type = input_2

    assert_that(gate.gate_type, equal_to(input_2))
    assert_that(gate.decomposition, equal_to(None))