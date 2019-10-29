import pytest
from pytest_mock import mocker
from hamcrest import *
import numpy as np

from src.objects.quantum_system import SystemType
from src.objects.qudit import Qudit
from tests.src.dirac_notation.constants import *


@pytest.mark.parametrize('input,expected_output', [
    (
        ket_00, [[], SystemType.simple]
    )
])
def test_init(input, expected_output):
    system = Qudit(input)

    assert_that(system.children_systems, equal_to(expected_output[0]))
    assert_that(system.system_type, equal_to(expected_output[1]))


@pytest.mark.parametrize('input', [
    (
        ket_0
    )
])
def test_init_fail(input):
    try:
        system = Qudit(input)
        pytest.fail()
    except AssertionError:
        pass
