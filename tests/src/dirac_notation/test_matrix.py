import pytest
from pytest_mock import mocker
from hamcrest import *

from src.dirac_notation.matrix import Matrix
from src.dirac_notation.ket import Ket
from src.dirac_notation.bra import Bra
from src.dirac_notation.constants import *


@pytest.mark.parametrize('input,expected_output', [
    (
        identity_matrix(2), 2
    )
])
def test_add(input, expected_output):
    assert_that(input.vector_space, equal_to(expected_output))


# Magic methods


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        identity_matrix(2), identity_matrix(2), 2 * identity_matrix(2)
    )
])
def test_add(input_1, input_2, expected_output):
    output = input_1 + input_2
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        identity_matrix(2), identity_matrix(2), zero_matrix(2, 2)
    )
])
def test_sub(input_1, input_2, expected_output):
    output = input_1 - input_2
    assert_that(output, equal_to(expected_output))

@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        Matrix([[1, 2],[3, 4]]), Matrix([[2, 0],[1, 2]]), Matrix([[4, 4],[10, 8]])
    ), (
        Matrix([[1, 2],[3, 4]]), 2, Matrix([[2, 4],[6, 8]])
    ), (
        Ket([1, 0]), 2, Ket([2, 0])
    ), (
        Bra([1, 0]), 2, Bra([2, 0])
    )
])
def test_mul(input_1, input_2, expected_output):
    output = input_1 * input_2
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        Matrix([[1, 2],[3, 4]]), Matrix([[2, 0],[1, 2]]), Matrix([[2, 4],[7, 10]])
    ), (
        Matrix([[1, 2],[3, 4]]), 2, Matrix([[2, 4],[6, 8]])
    ), (
        Ket([1, 0]), 2, Ket([2, 0])
    ), (
        Bra([1, 0]), 2, Bra([2, 0])
    )
])
def test_rmul(input_1, input_2, expected_output):
    output = input_2 * input_1
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        Matrix([[1, 2],[3, 4]]), 2, Matrix([[0.5, 1],[1.5, 2]])
    ), (
        Ket([1, 0]), 2, Ket([0.5, 0])
    ), (
        Bra([1, 0]), 2, Bra([0.5, 0])
    )
])
def test_truediv(input_1, input_2, expected_output):
    output = input_1 / input_2
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        Matrix([[1, 2],[3, 4]]), Matrix([[1, 2],[3, 4]]), True
    ), (
        Matrix([[1, 2],[3, 4]]), Matrix([[1, 1],[3, 4]]), False
    ), (
        Ket([1, 0]), Ket([1, 0]), True
    ), (
        Bra([1, 0]), Ket([1, 0]), False
    )
])
def test_eq(input_1, input_2, expected_output):
    output = input_1 == input_2
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        Matrix([[1, 2],[3, 4]]), Matrix([[1, 2],[3, 4]]), False
    ), (
        Matrix([[1, 2],[3, 4]]), Matrix([[1, 1],[3, 4]]), True
    ), (
        Ket([1, 0]), Ket([1, 0]), False
    ), (
        Bra([1, 0]), Ket([1, 0]), True
    )
])
def test_ne(input_1, input_2, expected_output):
    output = (input_1 != input_2)
    assert_that(output, equal_to(expected_output))