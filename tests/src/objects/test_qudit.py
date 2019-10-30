import pytest
from pytest_mock import mocker
from hamcrest import *
import numpy as np

from src.objects.quantum_system import SystemType
from src.objects.qudit import Qudit
from src.dirac_notation.constants import *


@pytest.mark.parametrize('input', [
    (
        comp_ket_x(0, 4)
    )
])
def test_init(input):
    system = Qudit(input)

    assert_that(system.children_systems, equal_to(None))
    assert_that(system.system_type, equal_to(SystemType.simple))


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



@pytest.mark.parametrize('input_1,input_2', [
    (
        comp_ket_x(0, 8), comp_ket_x(0, 4)
    )
])
def test_children_systems_1(input_1, input_2):
    system = Qudit(input_1)
    child_system = Qudit(input_2)
    system.children_systems = [child_system]

    assert_that(system.children_systems, equal_to([child_system]))
    assert_that(system.system_type, equal_to(SystemType.product))


@pytest.mark.parametrize('input', [
    (
        comp_ket_x(0, 8)
    )
])
def test_children_systems_2(input):
    system = Qudit(input)
    system.children_systems = []
    system.children_systems = None

    assert_that(system.children_systems, equal_to(None))
    assert_that(system.system_type, equal_to(SystemType.simple))