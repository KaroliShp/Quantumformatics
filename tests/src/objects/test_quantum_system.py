import pytest
from pytest_mock import mocker
from hamcrest import *
import numpy as np

from src.objects.quantum_system import QuantumSystem, SystemType
from tests.src.dirac_notation.constants import *


@pytest.mark.parametrize('input,expected_output', [
    (
        ket_0, [ket_0, None, SystemType.simple, 2]
    )
])
def test_init(input, expected_output):
    system = QuantumSystem(input)

    assert_that(system.state, equal_to(expected_output[0]))
    assert_that(system.parent_system, equal_to(expected_output[1]))
    assert_that(system.system_type, equal_to(expected_output[2]))
    assert_that(system.vector_space, equal_to(expected_output[3]))


@pytest.mark.parametrize('input_1,input_2', [
    (
        ket_0, ket_1
    )
])
def test_parent_system_error(input_1, input_2):
    system = QuantumSystem(input_1)
    system.parent_system = input_2
    try:
        system.parent_system = input_2
        pytest.fail()
    except ValueError:
        pass
