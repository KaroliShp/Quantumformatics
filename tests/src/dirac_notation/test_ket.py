import pytest
from pytest_mock import mocker
from hamcrest import *
import numpy as np

from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix


@pytest.mark.parametrize('input_1,input_2,expected_output_1,expected_output_2', [
    (
        Ket([1,1]), 
        [
            Ket([1,0]), Ket([0,1])
        ],
        True,
        [ 
            1, 1
        ]
    ), (
        Ket([1,1]), 
        [
            Ket([1,0]), Ket([2,0])
        ],
        False, 0
    )
])
def test_linear_combination(input_1, input_2, expected_output_1, expected_output_2):
    output = input_1.linear_combination(input_2)
    assert_that(output[0], equal_to(expected_output_1))
    np.testing.assert_array_equal(output[1], expected_output_2)


# Magic methods


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        Matrix([[1, 0],[0, 1]]), Ket([0, 1]), Ket([0, 1])
    )
])
def test_rmul(input_1, input_2, expected_output):
    output = input_1 * input_2
    assert_that(output, equal_to(expected_output))