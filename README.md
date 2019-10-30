# Quantumformatics

[![Build Status](https://travis-ci.com/KaroliShp/Quantumformatics.svg?token=H6dNDzgb7zQyC23kvSsb&branch=master)](https://travis-ci.com/KaroliShp/Quantumformatics)
[![codecov](https://codecov.io/gh/KaroliShp/Quantumformatics/branch/master/graph/badge.svg)](https://codecov.io/gh/KaroliShp/Quantumformatics)

Framework for simulating quantum information and computation theory on classic systems (educational purposes)

DEVELOPMENT CURRENTLY IN PROGRESS

## Table of Contents

- [Example](#Example)
- [Setup](#Setup)
- [Design](#Design)
- [Dirac (bra-ket) notation](#Dirac-bra-ket-notation)
- [Repository issues](#Repository-Issues)

## Example

Photon polarization example, can be found in `src/main.py`:

```python
# Set up the system
qubit_A = Qubit(const.ket_0)  # Vertical polarization, |0>
qubit_B = Qubit(const.ket_1)  # Horizontal polarization, |1>
computational_basis = Basis([const.ket_0, const.ket_1])  # Polarising filter 1, {|0>, |1>}
fourier_basis = Basis([const.ket_plus, const.ket_minus]) # Polarising filter 2, {|+>, |->}

# Check the probabilities of a vertically polarized photon passing
# through vertical and horizontal filters 
p_1 = get_probabilities(computational_basis, qubit_A)
assert p_1[0] == 1  # Vertically polarized photon will pass with probability 1
assert p_1[1] == 0  # Horizontally polarized photon will never pass filter

# Check the probabilities of a vertically polarized photon passing
# through filters at 45 degrees angles
p_2 = get_probabilities(fourier_basis, qubit_A)
assert p_2[0] == 0.5  # Vertically polarized photon will pass with probability 1/2
assert p_2[1] == 0.5  # Vertically polarized photon will pass with probability 1/2

# Perform measurement on A in computational basis
# and check that it is indeed in state 0 after the measurement
measure(computational_basis, qubit_A)
assert qubit_A.state == const.ket_0

# Perform measurement on B in fourier basis and print the resulting state of the qubit
outcome = measure(fourier_basis, qubit_B)
print(outcome)  # either 0 or 1
dirac.print(qubit_B.state)  # either |+> or |->, depending on the outcome
```

More experiments can be found in `src/experiments`.

## Setup

Language: Python 3.6+

```shell
$ git clone https://github.com/KaroliShp/Quantumformatics
$ cd Quantumformatics
$ pip install requirements.txt
```

You can play with the framework by using `src/main.py` file:

```shell
$ python src/main.py
```

Run tests:

```shell
$ pytest --cov=src
```

## Design

### Quantum systems

Quantum systems are represented by `Qubit` and `Qudit` classes, as the name suggest representing 2-dimensional and N-dimensional complex vector spaces respectively. Quantum system has a `state`, which is a `Ket`, and a `system_type` of the system state they are describing, more specifically `SystemType.simple`, `SystemType.product` and  `SystemType.entangled`:

```python
qubit_A = Qubit(ket_0)
# |0>
qubit_A.system_type
# SystemType.simple
```

We can define compositions of quantum systems to define product states:

```python
qubit_B = Qubit(ket_0)
# |0>
system_AB = create_composite_system(qubit_A, qubit_B)
# |00> = |0> ⊗ |0> = ( 1 0 0 0 )
system_AB.system_type
# SystemType.product
system_AB.children_systems
# [ qubit_A, qubit_B ]
qubit_A.parent_system
# system_AB
```

In the above example, `system_AB` is itself a `Qudit` representing 4-dimensional complex vector space, composed of `qubit_A` and `qubit_B`. All systems have references pointing to each other.

### Quantum gates

Quantum gates are described by `Gate` class. Gates have unitary `matrix`, which are of type `Matrix`, and `gate_type` describing the type of the gate, more specifically `GateType.simple`, `GateType.product` and `GateType.interaction`:

```python
unitary_matrix = (ket_plus * bra_0) + (ket_minus * bra_1)
hadamard_gate = Gate(unitary_matrix)
# H = |+><0| + |-><1|
hadamard_gate.gate_type
# GateType.simple
```

You can combine multiple gates to product gates for product measurements:

```python
identity_gate = Gate(identity_matrix)
# I = ( 1 0 / 0 1 )
product_gate = create_product_gate(hadamard_gate, identity_gate)
# U = H ⊗ I
product_gate.gate_type
#GateType.product
```

Currently, interaction gates are only supported as custom gates. The main reason behind this at the moment is the complexity of evaluating entangling states and correct products. This will be done later. The implementations for most important interaction gates and their entangling properties are predefined:

```python
cnot_gate = dirac.tensor(ket_0 * bra_0, identity_matrix) + dirac.tensor(ket_1 * bra_1, pauli_x_matrix)
# CNOT = |0><0| tensor I + |1><1| tensor X
cnot_gate.gate_type
# GateType.interaction
```

### Applying Quantum Gates

Module `actions.py` define all the required functions to apply gates on systems. Simple gates:

```python
qubit_A.state
# |0>
apply_simple_gate(hadamard_gate, qubit_A)
qubit_A.state
# |+>
```

Product gates (gate applies on the object that represents the system as a whole and its constituent parts):

```python
system_AB.state
# |00> = |0> ⊗ |0> = ( 1 0 0 0 )
product_gate.matrix
# U = H ⊗ I
apply_product_gate(product_gate, system_AB)
system_AB
# U|00> = H|0> ⊗ I|0>
system_AB.system_type
# SystemType.product
qubit_A.state
# H|0>
qubit_B.state
# I|0>
```

Interaction gates:

```python
qubit_C = Qubit(ket_plus)
# |+>
qubit_D = Qubit(ket_0)
# |0>
system_CD = create_composite_system(qubit_C, qubit_D)
# |+> ⊗ |0>
apply_interaction_gate(cnot_gate, system_CD)
system_CD
# |psi_plus>
system_CD.system_type
# SystemType.entangled
qubit_C.state
# None - represents a mixed state at the moment
qubit_D.state
# None
```

### Measurements

TODO


## Dirac (bra-ket) notation

Dirac notation is a convenient notation used to represent linear algebra operations in a human readable format for quick computation by hand. The purpose of Dirac notation in this repository is to increase readability and usability of the package for the users. You can describe and read quantum states/gates/etc. in terms of kets and bras, which on computer is way simpler than trying to read and input multidimensional arrays.

### Example

```python
import math

from src.dirac_notation.bra import Bra
from src.dirac_notation.ket import Ket
from src.dirac_notation.matrix import Matrix
from src.dirac_notation import functions as dirac


# Create Kets representing basic states
ket_0 = comp_ket_x(0, 2)  # |0> = ( 1 0 )
ket_1 = comp_ket_x(1, 2)  # |1> = ( 0 1 )
ket_psi_00 = dirac.tensor(ket_0, ket_0)  # |psi_00> = ( 1 0 0 0 )
ket_psi_01 = dirac.tensor(ket_0, ket_1)  # |psi_01> = ( 0 1 0 0 )
ket_psi_10 = dirac.tensor(ket_1, ket_0)  # |psi_10> = ( 0 0 1 0 )
ket_psi_11 = dirac.tensor(ket_1, ket_1)  # |psi_11> = ( 0 0 0 1 )

# Create a Ket representing an entangled state
ket_phi_x = (1 / math.sqrt(2)) * ((dirac.tensor(ket_0, ket_0)) + (dirac.tensor(ket_1, ket_1)))
ket_phi_y = (1 / math.sqrt(2)) * (ket_psi_00 + ket_psi_11)
bra_phi_y = (1 / math.sqrt(2)) * (Bra(ket_psi_00) + Bra(ket_psi_11))

# Magic
assert ket_phi_x == ket_phi_y
assert Bra(ket_phi_y) == bra_phi_y
dirac.print(ket_phi_x, [ket_psi_00, ket_psi_01, ket_psi_10, ket_psi_11])
# Output: value = 0.71 |psi_00> + 0.71 |psi_11> ; vector space = C^4 ; length = 1.0
```

### Design

`Matrix` class represents an arbitrary matrix in a d-dimensional Hilbert space. `Ket` and `Bra` classes are derived from `Matrix` class and represent column and row vectors respectively. 

`Matrix` implementation uses NumPy package under the hood to hold the values and perform calculations, acting sort of like a wrapper around NumPy functions. The current reason behind composition instead of direct inheritence from `np.ndarray` is that not all funcitonality is required and/or applicable to the use case, but this may change in the future. The main motivation behind having distinct `Ket` and `Bra` classes is the fact that NumPy does not support column vectors natively (all vectors are treated as `(n,)` shape `np.ndarray`), which makes it harder to write matrices in bra-ket notation.

### Usage

Basic objects can be created from `list` and `np.ndarray` objects, `Bra` object can also be created from `Ket` (using adjoint operation):

```python
ket_0 = Ket([1, 0])  # |0>
ket_1 = Ket([0, 1])  # |1>

bra_0 = Bra([1, 0]) = Bra(ket_0)  # <0|, created from |0>
bra_1 = Bra([0, 1]) = Bra(ket_1)  # <1|, created from |1>

identity = Matrix(np.array([[1,0], [0, 1]]))  # I = [ 1 0 / 0 1 ]
```

You can use arithmetic and comparison operators on these objects and therefore construct new objects:

```python
ket_x = ket_0 + ket_1  # |0> + |1>
ket_y = 2 * ket_x  # 2|0> + 2|1>
product = bra_0 * ket_0  # 1
matrix = ket_0 * bra_0  # |0><0| = [ 1 0 / 0 0 ]
```

You can either use the operators to perform mathematical functions, or you can use functions (additional functions as well) provided in the `functions.py` file.

```python
from src.dirac_notation import functions as dirac

dirac.add(ket_0, ket_1) == ket_0 + ket_1  # True
dirac.tensor(ket_0, ket_0) # |0> tensor |0> = |psi00>
```

Dirac notation also supports human-readable output with any chosen vectors. The output is a linear combination of vectors `|0>, |1>, ..., |n>` by default, you can also choose decimal precision and more information:

```
>>> dirac.print(ket_0)
|0> = |0>
>>> dirac.print(ket_0, [ket_0, ket_1])
|0> = |0>
>>> dirac.print(ket_0, [fourier_ket_0, fourier_ket_1], precision = 2)
|0> = 0.71 |+> + 0.71 |->
>>> dirac.print(ket_0, [fourier_ket_0, fourier_ket_1], precision = 2, info = True)
value = 0.71  |0> + 0.71  |1> ; vector space = C^2 ; length = 1.0
```

### Constants

Just like the package comes with predefined qubits, gates and systems, so does Dirac notation, which is, in fact, used to predefine the aforementioned quantum systems (`from src.dirac_notation import constants as const`). It contains objects of `Ket`, `Bra` and `Matrix`

```python
>>> const.ket_0
# |0>
>>> const.ket_plus
# |+>
>>> const.comp_ket_x(1, 2)
# |1>
>>> 
```

## Repository issues

List of repository issues, which are just observations and thoughts, rather than the "GitHub issues"

### Compositions of quantum systems are very messy:

- A system can belong to infinite amount of other systems
- A system can also be comprised of infinite amount of other systems
- Measurement/reversible process on one of those consituents affects all involved parts

Current solution to quantum systems: can only belong to one parent at one point in time (which can belong to one parent etc.). In this way, we dont have an infinite number of states. Gate application is then significantly easier as well.

### Interaction gates are not as trivial as I thought they were

- Not all interaction gates are entangling (and I don't yet know if it is possible to figure out all states that are entangled by an interaction gate)
- Interaction gates applied on entangled states (if this is legit) may not necessarily keep those states entangled
- Hardest step is computation - when a gate is an interaction gate, it cannot be expressed as a product of two states. So after applying an interaction gate to a product state that remains a product state, how do we figure out numerically what happens to each state?
- If you apply entangling gate to a state that is compromised of product states, does it mean that all consituents are entangled?
- What happens when product states are made of entangled states that are made of product states (recursion)

Current solution to interaction gates: must be predefined.


### No representation of mixed states

- Did not have time to read about this yet

### Human readable output needs some work on notation

- Did not have time to make it prettier