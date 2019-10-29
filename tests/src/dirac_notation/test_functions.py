import pytest
from pytest_mock import mocker
from hamcrest import *
import numpy as np

from src.dirac_notation.ket import Ket
from src.dirac_notation.bra import Bra
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from tests.src.dirac_notation.constants import *


# Type functions


@pytest.mark.parametrize('input,expected_output', [
    (
        bra_0, True 
    ), (
        identity_matrix, False
    )
])
def test_is_bra(input, expected_output):
    output = dirac.is_bra(input)
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input,expected_output', [
    (
        ket_0, True 
    ), (
        identity_matrix, False
    )
])
def test_is_ket(input, expected_output):
    output = dirac.is_ket(input)
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input,expected_output', [
    (
        identity_matrix, True
    ), (
        ket_0, False
    ), (
        bra_0, False
    )
])
def test_is_matrix(input, expected_output):
    output = dirac.is_matrix(input)
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        ket_0, ket_1, True
    ),
    (
        identity_matrix, ket_1, False
    )
])
def test_is_same(input_1, input_2, expected_output):
    output = dirac.is_same(input_1, input_2)
    assert_that(output, equal_to(expected_output))


# Arithmetic operations


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        bra_0, ket_0, 1
    ), (
        bra_0, ket_1, 0
    )
])
def test_braket(input_1, input_2, expected_output):
    output = dirac.braket(input_1, input_2)
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input,expected_output', [
    (
        [ket_0, ket_0], Ket([1, 0, 0, 0])
    ), (
        [bra_0, bra_0], Bra([1, 0, 0, 0])
    ), (
        [ket_0, ket_0, ket_0], Ket([1, 0, 0, 0, 0, 0, 0, 0])
    ), (
        [identity_matrix, identity_matrix], Matrix(np.identity(4))
    )
])
def test_tensor(input, expected_output):
    output = dirac.tensor(*input)
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input,expected_output', [
    (
        ket_0, bra_0
    ), (
        bra_0, ket_0
    ), (
        identity_matrix, identity_matrix
    ), (
        Ket([1j, 0]), Bra([-1j, 0])
    ), (
        Matrix([[1j, 1j], [0, 1]]), Matrix([[-1j, 0], [-1j, 1]])
    )
])
def test_adjoint(input, expected_output):
    output = dirac.adjoint(input)
    assert_that(output, equal_to(expected_output))


# Information functions


@pytest.mark.parametrize('input,expected_output', [
    (
        ket_0, True
    ), (
        2 * bra_0, False
    )
])
def test_is_unit(input, expected_output):
    output = dirac.is_unit(input)
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input,expected_output', [
    (
        identity_matrix, True
    ), (
        pauli_x_matrix, True
    ), (
        Matrix([[1, 1], [1, 0]]), False
    )
])
def test_is_unitary(input, expected_output):
    output = dirac.is_unitary(input)
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        ket_0, ket_0, False
    ), (
        bra_0, bra_1, True
    )
])
def test_is_orthogonal(input_1, input_2, expected_output):
    output = dirac.is_orthogonal(input_1, input_2)
    assert_that(output, equal_to(expected_output))


@pytest.mark.parametrize('input_1,input_2,expected_output', [
    (
        ket_0, ket_0, False
    ), (
        2*bra_0, bra_1, False
    ), (
        ket_0, ket_1, True
    )
])
def test_is_orthonormal(input_1, input_2, expected_output):
    output = dirac.is_orthonormal(input_1, input_2)
    assert_that(output, equal_to(expected_output))