import pytest
from pytest_mock import mocker
from hamcrest import *

from src.dirac_notation.matrix import Matrix
from src.dirac_notation.ket import Ket
from src.dirac_notation.bra import Bra
from src.dirac_notation import constants as const
from tests.src.dirac_notation import constants as t_const


# Kets and Bras


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        0, 2, t_const.ket_0
    ), (
        1, 2, t_const.ket_1
    ), (
        2, 2, None
    )
])
def test_comp_ket(input_1, input_2, expected_output):
    output = const.comp_ket_x(input_1, input_2)
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        0, 2, t_const.bra_0
    ), (
        1, 2, t_const.bra_1
    ), (
        2, 2, None
    )
])
def test_comp_bra(input_1, input_2, expected_output):
    output = const.comp_bra_x(input_1, input_2)
    assert_that(output, equal_to(expected_output))