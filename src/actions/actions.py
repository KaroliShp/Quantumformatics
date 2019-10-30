import math
from typing import List
from functools import reduce

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


def create_composite_system(*qudits: QuantumSystem) -> QuantumSystem:
    """
    Create a composite system from a number of composite systems
    """
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


def create_entangled_system(state: Ket, *qudits: QuantumSystem) -> QuantumSystem:
    """
    Create an entangled system from a number of composite systems
    """
    assert qudits and len(qudits) >= 2
    assert not (False in [isinstance(qudit, QuantumSystem) for qudit in qudits])
    assert state.vector_space == reduce(lambda x, y : x + y, list(map(lambda z : z.vector_space, qudits)))
    # assert that state is actually entangled

    # Create entangled system
    composite_system = Qudit(state)
    composite_system.children_systems = list(qudits)
    composite_system.system_type = SystemType.entangled

    # Assign the parent to qudits and make their children enter entanglement
    for qudit in qudits:
        qudit.parent_system = composite_system
        _enter_entanglement(qudit)

    return composite_system


def _enter_entanglement(qudit: QuantumSystem) -> None:
    """
    All dependent underlying systems become entangled once the composition is entangled
    """
    assert isinstance(qudit, QuantumSystem)
    
    if qudit.system_type != SystemType.simple:
        # Turn children into mixed state and apply entanglement on them
        for child in qudit.children_systems:
            child.state = None
            _enter_entanglement(child)
        
        # Subsystem is now also entangled
        qudit.system_type = SystemType.entangled


# Reversable processes


def create_product_gate(*gates: Gate) -> Gate:
    """
    Create product gate from other gates
    """
    product_state = dirac.tensor(*list(map(lambda z : z.matrix, gates)))
    product_gate = Gate(product_state)
    product_gate.decomposition = list(gates)
    return product_gate


def apply_interaction_gate(gate: Gate, qudit: QuantumSystem) -> None:
    """
    Apply interaction gate to a quantum system

    Simplification: only allow interaction gate on product systems
    """
    assert isinstance(gate, Gate) and isinstance(qudit, QuantumSystem)
    assert gate.gate_type == GateType.interaction and qudit.system_type == SystemType.product
    assert gate.vector_space == qudit.vector_space

    # Check if the system becomes entangled and assign state
    entanglement, new_state = gate.interact(*qudit.children_systems)

    # If gate is entangling and system was a product, system goes into entangled state
    if qudit.system_type == SystemType.product and entanglement:
        qudit.state = new_state
        _enter_entanglement(qudit)
    # If gate is entangling and system already was entangled just change the state
    elif qudit.system_type == SystemType.entangled and entanglement:
        qudit.state = new_state
    # If gate creates a state that is no longer entangled
    elif qudit.system_type == SystemType.entangled and not entanglement:
        return NotImplemented
    # If gate acts on a state that was never entangled
    elif qudit.system_type == SystemType.product and not entanglement:
        # Gates like SWAP, CNOT, currently do nothing
        qudit.state = dirac.tensor(*new_state)
        for i, child in enumerate(qudit.children_systems):
            child.state = new_state[i]
        # Finish implementing effects on their child systems
    else:
        return NotImplemented


def apply_product_gate(gate: Gate, qudit: QuantumSystem) -> None:
    """
    Apply product gate to a product system
    """
    assert isinstance(gate, Gate) and isinstance(qudit, QuantumSystem)
    assert gate.gate_type == GateType.product and qudit.system_type == SystemType.product
    assert gate.vector_space == qudit.vector_space
    assert len(gate.decomposition) == len(qudit.children_systems)

    # Apply on the system as a whole
    qudit.state = gate.matrix * qudit.state

    # Apply on the individual qubits (that may also be composite systems themselves)
    for i in range(0, len(gate.decomposition)):
        # Both are simple
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
        try:
            apply_interaction_gate(gate.decomposition[i], qudit.children_systems[i])
        except:
            return NotImplemented


def apply_simple_gate(gate: Gate, qudit: QuantumSystem) -> None:
    """
    Apply simple gate to a simple quantum system
    """
    assert isinstance(gate, Gate) and isinstance(qudit, QuantumSystem)
    assert gate.gate_type == GateType.simple and qudit.system_type == SystemType.simple
    assert gate.vector_space == qudit.vector_space

    """
    # TODO fix this in the future
    if qudit.has_parent_system:
        print('Careful, the system has a parent system which will be affected by this gate')
    """

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