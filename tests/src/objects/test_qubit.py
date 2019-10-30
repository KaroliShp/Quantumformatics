import pytest
from pytest_mock import mocker
from hamcrest import *
import numpy as np

from src.objects.quantum_system import SystemType
from src.objects.qubit import Qubit
from src.dirac_notation.constants import *


@pytest.mark.parametrize('input,expected_output', [
    (
        ket_0, SystemType.simple
    )
])
def test_init(input, expected_output):
    system = Qubit(input)

    assert_that(system.system_type, equal_to(expected_output))


@pytest.mark.parametrize('input', [
    (
        comp_ket_x(0, 4)
    )
])
def test_init_fail(input):
    try:
        system = Qubit(input)
        pytest.fail()
    except AssertionError:
        pass
