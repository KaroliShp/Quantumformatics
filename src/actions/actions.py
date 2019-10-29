import math
from typing import List

import numpy as np

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac
from src.dirac_notation import constants as const
from src.objects.gate import Gate, GateType
from src.objects.qubit import Qubit
from src.objects.qudit import Qudit
from src.objects.quantum_system import QuantumSystem, SystemType
from src.objects.basis import Basis


# Quantum systems


def create_composite_system(*qudits) -> Qudit:
    assert qudits and len(qudits) >= 2
    assert not (False in [isinstance(qudit, QuantumSystem) for qudit in qudits])

    # Create composite system
    composite_state = dirac.tensor(*list(map(lambda x : x.state, qudits)))
    composite_system = Qudit(composite_state)
    composite_system.children_systems = list(qudits)

    # Assign the parent to qudits
    for qudit in qudits:
        qudit.parent_system = composite_state

    return composite_system


# Reversable processes


def apply_interaction_gate(gate: Gate, qudit: QuantumSystem) -> None:
    assert isinstance(gate, Gate) and isinstance(qudit, QuantumSystem)
    assert gate.type == GateType.interaction or gate.type == GateType.entangling
    assert qudit.type == SystemType.product or qudit.type == SystemType.entangled
    assert gate.vector_space == qudit.vector_space

    # Apply on the system as a whole
    qudit.state = gate.matrix * qudit.state

    # If the gate is entangling and system was a product, system goes into entangled state
    if gate.type == GateType.entangling and qudit.type == SystemType.product:
        qudit.system_type == SystemType.entangled
        enter_entanglement(qudit)

    # Handle case with interaction gate that creates a state that is no longer entangled


def _enter_entanglement(qudit: QuantumSystem):
    """
    All dependent underlying systems become entangled once the composition is entangled
    """
    assert type(qudit) == QuantumSystem
    for child in qudit.children_systems:
        child.state = None  # Mixed state
        become_entangled(child)


def apply_product_gate(gate: Gate, qudit: QuantumSystem) -> None:
    """
    Product gate applied to a product system
    """
    assert isinstance(gate, Gate) and isinstance(qudit, QuantumSystem)
    assert gate.gate_type == GateType.product
    assert qudit.system_type == SystemType.product
    assert gate.vector_space == qudit.vector_space
    assert len(gate.decomposition) == len(qudit.children_systems)

    # Apply on the system as a whole
    qudit.state = gate.matrix * qudit.state

    # Apply on the individual qubits (that may also be composite systems)
    for i in range(0, len(gate.decomposition)):
        # Both are simple
        apply_simple_gate(gate.decomposition[i], qudit.children_systems[i])
        try:
            apply_simple_gate(gate.decomposition[i], qudit.children_systems[i])
            continue
        except:
            pass

        # Both are product
        try:
            apply_product_gate(gate.decomposition[i], qudit.children_systems[i])
            continue
        except:
            pass
        
        # Both are composite
        apply_interaction_gate(gate.decomposition[i], qudit.children_systems[i])


def apply_simple_gate(gate: Gate, qudit: QuantumSystem) -> None:
    """
    Simple gate applied to a simple quantum system
    
    Simplification: to avoid problems with qudits in composite systems, currently
    it is not allowed to apply a simple gate on a qubit that belongs to a composite system
    """
    assert isinstance(gate, Gate) and isinstance(qudit, QuantumSystem)
    assert gate.gate_type == GateType.simple
    assert qudit.system_type == SystemType.simple
    assert gate.vector_space == qudit.vector_space

    qudit.state = gate.matrix * qudit.state


# Basic measurements


def get_probability_distribution(basis: Basis, qudit: Qudit) -> list:
    """
    Get probabilities of qudit measurement on the chosen ONB
    """
    assert isinstance(basis, Basis) and isinstance(qudit, Qudit)
    assert basis.vector_space == qudit.vector_space
    
    # Obtain probabilities and assert the sum of 1
    result = np.zeros(basis.vector_space)
    for i in range(0, basis.vector_space):
        result[i] = abs(Bra(basis.states[i]) * qudit.state) ** 2
    assert math.isclose(sum(result), 1, abs_tol = 0.02)

    # Hacky way to make it sum up to 1 perfectly (fix later)
    if sum(result) > 1.0:
        result[-1] -= sum(result) - 1.0
    elif sum(result) < 1.0:
        result[-1] += 1.0 - sum(result)

    return np.round(result, decimals=2) # TODO fix rounding


def measure(basis: Basis, qudit: Qudit) -> int:
    """
    Measure qudit on a chosen ONB
    """
    # Obtain probabilities
    result = get_probabilities(basis, qudit)

    # Obtain the outcome
    outcome = np.random.choice(result.shape[0], 1, p = result)[0]

    # Change qudit state
    set_state(basis.states[outcome], qudit)

    return outcome