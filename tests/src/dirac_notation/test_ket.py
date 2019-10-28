import pytest
from pytest_mock import mocker
from hamcrest import *

from src.dirac_notation.ket import Ket


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        Ket([1, 0]), Ket([0, 1]), Ket([1, 1])
    ), (
        Ket([1, 1, 1]), Ket([1, 1, 1]), Ket([2, 2, 2])
    )
])
def test_addition(input_1, input_2, expected_output):
    # Act
    output = input_1 + input_2

    # Assert
    assert_that(output, equal_to(expected_output))