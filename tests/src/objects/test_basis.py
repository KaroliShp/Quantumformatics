import pytest
from pytest_mock import mocker
from hamcrest import *
import numpy as np

from src.objects.basis import Basis
from src.dirac_notation.constants import *


@pytest.mark.parametrize('input,expected_output', [
    (
        [comp_ket_x(0, 2), comp_ket_x(1, 2)], 2
    )
])
def test_init(input, expected_output):
    basis = Basis(input)

    assert_that(basis.states, equal_to(input))
    assert_that(basis.vector_space, equal_to(expected_output))


@pytest.mark.parametrize('input', [
    (
        [comp_ket_x(0, 2), comp_ket_x(0, 2)]
    ), (
        [comp_ket_x(0, 4), comp_ket_x(1, 4)]
    )
])
def test_init_fail(input):
    try:
        basis = Basis(input)
        pytest.fail()
    except AssertionError:
        pass
