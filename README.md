# Quantumformatics

[![Build Status](https://travis-ci.com/KaroliShp/Quantumformatics.svg?token=H6dNDzgb7zQyC23kvSsb&branch=master)](https://travis-ci.com/KaroliShp/Quantumformatics)

(Educational) framework for simulating quantum information and computation theory.

DEVELOPMENT CURRENTLY IN PROGRESS

## Table of Contents

- [Example](#Example)
- [Setup](#Setup)
- [Design](#Design)
- [Dirac (bra-ket) notation](#Dirac-bra-ket-notation)

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

TODO

## Dirac (bra-ket) notation

Dirac notation is a convenient notation to represent linear algebra concepts, such as row and column vectors, matrices and linear algebra operations, in a human readable format for quick computation by hand. The purpose of Dirac notation in this repository is to increase readability and usability of the package for the users. You can describe and read quantum states/gates/etc. in terms of kets and bras, which on computer is way simpler than trying to read and input multidimensional arrays.

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

`Matrix` class represents an arbitrary matrix in a d-dimensional Hilbert space. `Ket` and `Bra` classes are derived from `Matrix` class and represent column and row vectors respectively. `Matrix` implementation uses `numpy` package under the hood (composition) to hold the values and perform calculations. The main motivation behind having distinct `Ket` and `Bra` classes is the fact that `numpy` does not support column vectors natively (all vectors are treated as `(n,)` shape `np.ndarray`), which makes it harder to write BraKet notation using it.

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